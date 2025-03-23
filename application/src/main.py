import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Carregar as credenciais do Google Sheets a partir do arquivo credentials.json
credentials_path = os.getenv('GOOGLE_SHEET_CREDENTIALS_PATH')
creds = Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/spreadsheets"])

# Autorizar o cliente do Google Sheets
gc = gspread.authorize(creds)

# IDs das planilhas de origem e destino (definidos no .env)
origin_sheet_id = os.getenv('GOOGLE_SHEET_ORIGIN_ID')
destination_sheet_id = os.getenv('GOOGLE_SHEET_DESTINATION_ID')

# Abrir as planilhas
origin_sheet = gc.open_by_key(origin_sheet_id).sheet1
destination_sheet = gc.open_by_key(destination_sheet_id).worksheet('FICHAS')

# Mapeamento de colunas entre a planilha de origem e destino
column_mapping = {
    "NOME COMPLETO": "NOME",
    "TELEFONE PARA CONTATO (de preferência whatsapp)": "TELEFONE",
    "NOME DE GUERRA": "APELIDO",
    "@ DO INSTAGRAM": "INSTAGRAM",
    "ESTADO CIVIL": "ESTADO CIVIL",
    "RELIGIÃO": "RELIGIÃO",
    "EMAIL": "EMAIL",
    "POSSUI ALGUM TIPO DE ALERGIA OU COMORBIDADE? SE SIM, DESCREVA ABAIXO. SE NÃO, RESPONDA COM NÃO.": "ALERGIA OU COMORBIDADE",
    "ESTARÁ COM VEÍCULO PRÓPRIO NOS DIAS DO ENCONTRO?": "EQUIPE",  # Adaptar conforme necessário
    "LIGAR PARA": "TEL EMERGENCIA",
    "PARENTESCO": "PARENTESCO",
    "NOME DO CONTATO DE EMERGÊNCIA": "NOME EMERGENCIA",
    "ESCOLHA A EQUIPE QUE DESEJA TRABALHAR:": "EQUIPE",  # Adaptar conforme necessário
    "QUAL O TAMANHO DA CAMISA?": "TAM CAMISA",
    "NOME DO PAGADOR:": "SITUAÇÃO",  # Adaptar conforme necessário
    "VALOR PAGO:": "PAGAMENTO",  # Adaptar conforme necessário
    "DATA DO PAGAMENTO": "OBSERVAÇÃO",  # Adaptar conforme necessário
    "ANEXE AQUI o comprovante de pagamento em PIX.": "OBSERVAÇÃO",
    "DETALHES DO PAGAMENTO": "OBSERVAÇÃO",
    "IGREJA QUE CONGREGA": "IGREJA"
}

# Classe auxiliar para manipulação das planilhas
class PlanilhaUtils:

    def __init__(self, origin_sheet, destination_sheet):
        self.origin_sheet = origin_sheet
        self.destination_sheet = destination_sheet

    def is_duplicate(self, name, phone):
        """
        Verifica se já existe uma entrada com o mesmo nome e telefone na planilha de destino.
        """
        destination_data = self.destination_sheet.get_all_values()
        for row in destination_data[2:]:  # Ignora cabeçalhos (linhas 1 e 2)
            dest_name = row[2]  # Índice 2 -> NOME
            dest_phone = row[5]  # Índice 5 -> TELEFONE
            if dest_name == name and dest_phone == phone:
                return True
        return False

    def write_to_destination(self, data):
        """
        Escreve os dados na planilha de destino.
        """
        current_id = len(self.destination_sheet.get_all_values()) - 1  # Desconta cabeçalho

        # Preparar a nova linha com os dados
        new_row = [current_id + 1]  # ID numérico crescente
        for col in column_mapping.keys():
            if col in data:
                new_row.append(data[col])
            else:
                new_row.append("")  # Caso o dado não esteja presente na origem

        # Escrever na planilha de destino
        self.destination_sheet.append_row(new_row)

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


if __name__ == "__main__":
    # Instancia a classe auxiliar com as planilhas de origem e destino
    planilha_utils = PlanilhaUtils(origin_sheet, destination_sheet)

    # Processar e transferir os dados
    planilha_utils.process_data()

    print("Dados processados e escritos na planilha de destino.")
