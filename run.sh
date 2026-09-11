#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

# Verifica se o .env existe
if [ ! -f ".env" ]; then
    echo "[ERRO] Arquivo .env nao encontrado!"
    echo "Certifique-se de que o arquivo .env esta na mesma pasta que este script."
    exit 1
fi

# Carrega variáveis do .env (leitura literal, sem interpretar como shell,
# pois valores como GOOGLE_SHEET_ORIGIN_ID usam ";" como separador)
set -a
while IFS='=' read -r key value || [ -n "$key" ]; do
    key="${key%$'\r'}"
    case "$key" in
        ''|'#'*) continue ;;
    esac
    value="${value%$'\r'}"
    export "$key=$value"
done < .env
set +a

# Verifica se o uv esta instalado
if ! command -v uv >/dev/null 2>&1; then
    echo "[ERRO] uv nao encontrado!"
    echo "Instale o uv (https://docs.astral.sh/uv/) antes de continuar."
    exit 1
fi

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "[ERRO] Ambiente virtual \".venv\" nao encontrado!"
    echo "Execute \"make install\" para cria-lo e instalar as dependencias."
    exit 1
fi

# Executa o main.py usando uv
uv run application/src/main.py
