# 📝 Sincronizador de Inscrições do Google Forms

Este projeto em Python tem como objetivo **ler respostas de um formulário do Google Forms** (armazenadas em uma planilha do Google Sheets) e sincronizá-las com uma **planilha de destino**, evitando duplicações com base no nome e telefone.

---

## ✅ Funcionalidades

- Lê automaticamente novas inscrições da planilha de origem.
- Compara com a planilha de destino, evitando duplicações.
- Gera um campo `ID` incremental na planilha de destino.
- Escreve os dados organizados na aba `FICHAS`, a partir da linha 3.
- Permite deploy para `.exe` (sem necessidade de Python instalado).

---

## ⚙️ Pré-requisitos

- Python 3.11+ instalado.
- Conta no [Google Cloud Console](https://console.cloud.google.com/).
- Permissão de leitura na planilha de origem.
- Permissão de escrita na planilha de destino.

---

## 🔐 Credenciais da API do Google

Para que o script consiga acessar e editar as planilhas, você deve:

1. Criar um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ativar a API **Google Sheets** e **Google Drive**.
3. Criar uma **credencial de conta de serviço** (`credentials.json`).
4. Compartilhar as planilhas de origem e destino com o e-mail gerado pela conta de serviço (algo como `minha-conta@meu-projeto.iam.gserviceaccount.com`).

---

## 📁 Estrutura esperada

```
.
├── application/
│   └── src/
│       ├── main.py
│       └── planilha_utils.py
├── credentials/
│   └── credentials.json
├── .env
├── Makefile
├── requirements.txt
└── README.md
```

---

## 🌍 Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
GOOGLE_SHEET_CREDENTIALS_PATH=..\..\credentials\credentials.json
GOOGLE_SHEET_ORIGIN_ID=<ID_PLANILHA_ORIGEM>
GOOGLE_SHEET_DESTINATION_ID=<ID_PLANILHA_DESTINO>
GOOGLE_SHEET_DESTINATION_WORKSHEET=FICHAS
```

> **Importante:** o `ID_DA_PLANILHA` é a parte do link entre `/d/` e `/edit`, por exemplo:
>
> ```
> https://docs.google.com/spreadsheets/d/1abcD34EFghij56K8vwXyZ9z0abcdEfGh/edit#gid=0
> ```
> O `ID` neste caso seria: `1abcD34EFghij56K8vwXyZ9z0abcdEfGh`

---

## 💻 Execução

### Durante o desenvolvimento

```bash
make install
make run
```

### Criar executável (`.exe`)

```bash
make deploy
```

O executável será gerado na pasta `dist/`.

---

## 📦 Dependências

Listadas no `requirements.txt`, incluindo:
- `gspread`
- `oauth2client`
- `python-dotenv`
