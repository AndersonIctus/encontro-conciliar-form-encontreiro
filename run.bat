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

REM Verifica se o venv existe
if not exist "venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual "venv" nao encontrado!
    echo Execute "make install" ou "python -m venv venv" e instale requirements.txt.
    pause
    exit /b 1
)

REM Executa o main.py usando o Python do venv
venv\Scripts\python.exe application\src\main.py

pause