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
- [uv](https://docs.astral.sh/uv/) instalado (gerencia o ambiente virtual e a execução do projeto).
- Conta no [Google Cloud Console](https://console.cloud.google.com/).
- Permissão de leitura na planilha de origem.
- Permissão de escrita na planilha de destino.

---

## 🔐 Credenciais da API do Google

Para que o script consiga acessar e editar as planilhas, você deve:

1. Criar (ou selecionar) um projeto no [Google Cloud Console](https://console.cloud.google.com/).
2. Ativar as APIs **Google Sheets** e **Google Drive** (menu "APIs e serviços" → "Biblioteca").
3. Criar uma **conta de serviço**: "APIs e serviços" → "Credenciais" → "Criar credenciais" → "Conta de serviço".
4. Gerar a chave: abra a conta de serviço criada → aba "Chaves" → "Adicionar chave" → "Criar nova chave" → formato **JSON**. O arquivo é baixado automaticamente.
5. Renomear o arquivo baixado para `credentials.json` e salvar em `credentials/credentials.json`.
6. Compartilhar as planilhas de origem e destino com o e-mail da conta de serviço (algo como `minha-conta@meu-projeto.iam.gserviceaccount.com`, encontrado no campo `client_email` do `credentials.json`), dando permissão de **Editor**. Ou seja, essa nova conta deve estar na sessão Compartilhamento como se fosse um usuário compartilhando a planilha com essa conta.

### Já tenho a conta de serviço, mas perdi o `credentials.json`

O Google **não permite reobter a chave privada** de um arquivo já baixado — só é possível gerar uma **nova chave** para a conta de serviço existente (passo 4 acima, na mesma conta). Isso não afeta o compartilhamento já feito nas planilhas, pois o e-mail da conta continua o mesmo.

> ⚠️ **Atenção:**
>
> - `credentials.json` contém uma chave privada — nunca deve ser commitado no Git (confira se está no `.gitignore`).
> - Se aparecer o erro `Caller does not have permission` ao rodar o script, normalmente falta compartilhar a planilha com o e-mail da conta de serviço (passo 6).

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
GOOGLE_SHEET_ORIGIN_ID=<ID_PLANILHA_ORIGEM_1>;<ID_PLANILHA_ORIGEM_2>
GOOGLE_SHEET_DESTINATION_ID=<ID_PLANILHA_DESTINO>
GOOGLE_SHEET_DESTINATION_WORKSHEET=FICHAS
```

> **Importante:** o `ID_DA_PLANILHA` é a parte do link entre `/d/` e `/edit`, por exemplo:
>
> ```
> https://docs.google.com/spreadsheets/d/1abcD34EFghij56K8vwXyZ9z0abcdEfGh/edit#gid=0
> ```
> O `ID` neste caso seria: `1abcD34EFghij56K8vwXyZ9z0abcdEfGh`
>
> **`GOOGLE_SHEET_ORIGIN_ID` aceita múltiplas planilhas de origem**, separadas por ponto-e-vírgula (`;`). O script processa cada uma delas, na ordem informada, escrevendo tudo na mesma planilha de destino e verificando duplicidade entre todas.

---

## 💻 Execução

### Durante o desenvolvimento

```bash
make install
make run
```

Ou, diretamente (Linux/macOS/Git Bash):

```bash
make install
./run.sh
```

No Windows (sem bash), use o `run.bat`.

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
