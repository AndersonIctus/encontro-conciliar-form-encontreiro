import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import sys
import time
from datetime import datetime

print("============================= S T A R T =============================")

# Resolve o caminho base: pasta do .exe quando empacotado (PyInstaller),
# pasta do main.py quando executado via "python main.py"
if getattr(sys, 'frozen', False):
    main_dir = os.path.dirname(sys.executable)
else:
    main_dir = os.path.dirname(os.path.abspath(__file__))

# Carregar variáveis de ambiente do arquivo .env
# (python-dotenv já detecta sys.frozen: usa cwd no .exe, sobe diretórios em modo dev)
load_dotenv()

# Carregar as credenciais do Google Sheets a partir do arquivo credentials.json
credentials_path = os.getenv('GOOGLE_SHEET_CREDENTIALS_PATH')

full_path = os.path.abspath(os.path.join(main_dir, credentials_path))

print("Usando credenciais em:", full_path)

creds = Credentials.from_service_account_file(full_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Autorizar o cliente do Google Sheets
gc = gspread.authorize(creds)

# IDs das planilhas de origem e destino (definidos no .env)
# GOOGLE_SHEET_ORIGIN_ID aceita uma lista de IDs separados por ponto-e-vírgula
origin_sheet_ids = [
    sheet_id.strip()
    for sheet_id in os.getenv('GOOGLE_SHEET_ORIGIN_ID', '').split(';')
    if sheet_id.strip()
]
destination_sheet_id = os.getenv('GOOGLE_SHEET_DESTINATION_ID')
destination_sheet_worksheet = os.getenv('GOOGLE_SHEET_DESTINATION_WORKSHEET')

# Abrir as planilhas
origin_sheets = [gc.open_by_key(sheet_id).sheet1 for sheet_id in origin_sheet_ids]
destination_sheet = gc.open_by_key(destination_sheet_id).worksheet(destination_sheet_worksheet)

# Mapeamento de colunas entre a planilha de origem e destino
column_mapping = {
    "Timestamp": "DT INSC",
    "NOME COMPLETO": "NOME",
    "NOME DE GUERRA": "APELIDO",
    "@ DO INSTAGRAM": "INSTAGRAM",
    "TELEFONE PARA CONTATO (de preferência whatsapp)": "TELEFONE",
    "ESTADO CIVIL": "ESTADO CIVIL",
    "IGREJA QUE CONGREGA": "IGREJA",
    "RELIGIÃO": "RELIGIÃO",
    "LIGAR PARA": "TEL EMERGENCIA",
    "NOME DO CONTATO DE EMERGÊNCIA": "NOME EMERGENCIA",
    "PARENTESCO": "PARENTESCO",
    "POSSUI ALGUM TIPO DE ALERGIA OU COMORBIDADE? SE SIM, DESCREVA ABAIXO. SE NÃO, RESPONDA COM NÃO.": "ALERGIA OU COMORBIDADE",
    "ESCOLHA A EQUIPE QUE DESEJA TRABALHAR:": "EQUIPE",  # Adaptar conforme necessário
    "QUAL O TAMANHO DA CAMISA?": "TAM CAMISA",
    "SITUACAO": "SITUAÇÃO",
    "ESTARÁ COM VEÍCULO PRÓPRIO NOS DIAS DO ENCONTRO?": "VEICULO",
    "DATA DO PAGAMENTO": "DT PAGAMENTO",
    "NOME DO PAGADOR:": "NOME PAGADOR",
    "VALOR PAGO:": "PAGAMENTO",  # Adaptar conforme necessário
    "DETALHES DO PAGAMENTO": "OBSERVAÇÃO",
    "MONTAGEM": "MONTAGEM",
}

# Limite de escritas por minuto na planilha de destino
MAX_WRITES_PER_MINUTE = 50

# Classe auxiliar para manipulação das planilhas
class PlanilhaUtils:

    def __init__(self, destination_sheet):
        self.destination_sheet = destination_sheet
        self.destination_data = self.destination_sheet.get_all_values()
        self.write_count = 0
        self.window_start = time.time()

    def _throttle_writes(self):
        """
        Garante que no máximo MAX_WRITES_PER_MINUTE escritas sejam feitas por minuto.
        Ao atingir o limite, aguarda o tempo restante da janela de 60s e zera o
        contador, liberando mais MAX_WRITES_PER_MINUTE escritas.
        """
        if self.write_count >= MAX_WRITES_PER_MINUTE:
            sleep_time = 60 - (time.time() - self.window_start)
            if sleep_time > 0:
                print(f"## Limite de {MAX_WRITES_PER_MINUTE} escritas por minuto atingido. "
                      f"Dormindo {sleep_time:.1f}s antes de continuar...")
                time.sleep(sleep_time)
            self.write_count = 0
            self.window_start = time.time()

    def is_duplicate(self, name, phone):
        """
        Verifica se já existe uma entrada com o mesmo nome e telefone na planilha de destino.
        """
        for row in self.destination_data[2:]:  # Ignora cabeçalhos (linhas 1 e 2)
            dest_name = row[2]  # Índice 2 -> NOME
            dest_phone = row[5]  # Índice 5 -> TELEFONE
            if dest_name == name and str(dest_phone) == str(phone):
                return True
        return False

    def write_to_destination(self, data):
        """
        Escreve os dados na planilha de destino.
        """
        current_id = len(self.destination_data) - 2  # Desconta cabeçalho

        # Preparar a nova linha com os dados
        new_row = [current_id + 1]  # ID numérico crescente
        for col in column_mapping.keys():
            if col in data:
                value = data[col]
                if col == 'ESCOLHA A EQUIPE QUE DESEJA TRABALHAR:' and str(value).startswith("TRÂNSITO"):
                    new_row.append("TRÂNSITO")
                elif col == 'ESCOLHA A EQUIPE QUE DESEJA TRABALHAR:' and str(value).startswith("BANDINHA"):
                    new_row.append("BANDINHA")
                elif col == 'VALOR PAGO:':
                    if float(value) == 0:
                        new_row.append(0)
                    else:
                        new_row.append(float(value)/100)
                elif col == 'DATA DO PAGAMENTO':
                    try:
                        payment_date = datetime.strptime(str(value), '%m/%d/%Y')
                        new_row.append(payment_date.strftime('%d/%m/%Y'))
                    except ValueError:
                        try:
                            payment_date = datetime.strptime(str(value), '%m/%d/%y')
                            new_row.append(payment_date.strftime('%d/%m/%Y'))
                        except ValueError:
                            new_row.append(value)
                else:
                    new_row.append(data[col])
            else:
                if col == 'SITUACAO':
                    new_row.append("PENDENTE")
                elif col == 'MONTAGEM':
                    new_row.append("NÃO VERIFICADO")
                else:
                    print(f"## Coluna '{col}' não encontrada na origem. Adicionando valor vazio.")
                    new_row.append("")  # Caso o dado não esteja presente na origem

        # Respeitar o limite de escritas por minuto antes de escrever
        self._throttle_writes()

        # Escrever na planilha de destino
        self.destination_sheet.append_row(new_row)
        self.destination_data.append(new_row)
        self.write_count += 1

    def process_data(self, origin_sheet):
        """
        Processa os dados da planilha de origem e os escreve na planilha de destino,
        verificando duplicatas.
        """
        origin_data = origin_sheet.get_all_records()
        index = 1

        for row in origin_data:
            name = row["NOME COMPLETO"]
            phone = row["TELEFONE PARA CONTATO (de preferência whatsapp)"]

            # Verificar se a linha já foi escrita
            if not self.is_duplicate(name, phone):
                self.write_to_destination(row)
                print(f"## ({index}) {name} - Incluído")
            else:
                print(f"## ({index}) {name} - Duplicado já Incluído anteriormente")
                
            index = index + 1


if __name__ == "__main__":
    # Instancia a classe auxiliar com a planilha de destino
    planilha_utils = PlanilhaUtils(destination_sheet)

    # Processar e transferir os dados de cada planilha de origem
    for origin_sheet in origin_sheets:
        planilha_utils.process_data(origin_sheet)

    print("Foram inscritos na planilha de destino: ", planilha_utils.write_count)
    print("Dados processados e escritos na planilha de destino.")
    print("============================= E N D =============================")
