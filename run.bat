@echo off
setlocal

REM Verifica se o .env existe
if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado!
    echo Certifique-se de que o arquivo .env esta na mesma pasta que este .bat.
    pause
    exit /b 1
)

REM Carrega variáveis do .env
for /f "tokens=1,* delims==" %%A in (".env") do (
    set "%%A=%%B"
)

REM Verifica se o uv esta instalado
where uv >nul 2>nul
if errorlevel 1 (
    echo [ERRO] uv nao encontrado!
    echo Instale o uv (https://docs.astral.sh/uv/) antes de continuar.
    pause
    exit /b 1
)

REM Verifica se o venv existe
if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual ".venv" nao encontrado!
    echo Execute "make install" para cria-lo e instalar as dependencias.
    pause
    exit /b 1
)

REM Executa o main.py usando uv
uv run application\src\main.py

pause