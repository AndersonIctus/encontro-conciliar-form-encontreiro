import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar as credenciais do Google Sheets a partir do arquivo credentials.json
credentials_path = os.getenv('GOOGLE_SHEET_CREDENTIALS_PATH')

# Resolve o caminho absoluto, baseado no local do main.py
main_dir = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.abspath(os.path.join(main_dir, credentials_path))

print("Usando credenciais em:", full_path)

creds = Credentials.from_service_account_file(full_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Autorizar o cliente do Google Sheets
gc = gspread.authorize(creds)

# IDs das planilhas de origem e destino (definidos no .env)
origin_sheet_id = os.getenv('GOOGLE_SHEET_ORIGIN_ID')
destination_sheet_id = os.getenv('GOOGLE_SHEET_DESTINATION_ID')
destination_sheet_worksheet = os.getenv('GOOGLE_SHEET_DESTINATION_WORKSHEET')

# Abrir as planilhas
origin_sheet = gc.open_by_key(origin_sheet_id).sheet1
destination_sheet = gc.open_by_key(destination_sheet_id).worksheet(destination_sheet_worksheet)

# Mapeamento de colunas entre a planilha de origem e destino
column_mapping = {
    "Carimbo de data/hora": "DT INSC",
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
    "VALOR PAGO:": "PAGAMENTO",  # Adaptar conforme necessário
    "DETALHES DO PAGAMENTO": "OBSERVAÇÃO",
}

# Classe auxiliar para manipulação das planilhas
class PlanilhaUtils:

    def __init__(self, origin_sheet, destination_sheet):
        self.origin_sheet = origin_sheet
        self.destination_sheet = destination_sheet
        self.destination_data = self.destination_sheet.get_all_values()

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
                if col == 'ESCOLHA A EQUIPE QUE DESEJA TRABALHAR:' and str(value).startswith("TRANDINHA"):
                    new_row.append("TRANDINHA")
                else:
                    new_row.append(data[col])
            else:
                if col == 'SITUACAO':
                    new_row.append("PENDENTE")
                else:
                    new_row.append("")  # Caso o dado não esteja presente na origem

        # Escrever na planilha de destino
        self.destination_sheet.append_row(new_row)
        self.destination_data.append(new_row)

    def process_data(self):
        """
        Processa os dados da planilha de origem e os escreve na planilha de destino,
        verificando duplicatas.
        """
        origin_data = self.origin_sheet.get_all_records()

        for row in origin_data:
            name = row["NOME COMPLETO"]
            phone = row["TELEFONE PARA CONTATO (de preferência whatsapp)"]

            # Verificar se a linha já foi escrita
            if not self.is_duplicate(name, phone):
                self.write_to_destination(row)
                print(f"## {name} - Incluído")
            else:
                print(f"## {name} - Duplicado já Incluído anteriormente")


if __name__ == "__main__":
    # Instancia a classe auxiliar com as planilhas de origem e destino
    planilha_utils = PlanilhaUtils(origin_sheet, destination_sheet)

    # Processar e transferir os dados
    planilha_utils.process_data()

    print("Dados processados e escritos na planilha de destino.")
