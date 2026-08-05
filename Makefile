# Definições
PYTHON=python
VENV=venv
VENV_PYTHON=$(VENV)/Scripts/python.exe
SRC=application/src
DIST=dist
MAIN_SCRIPT=$(SRC)/main.py
EXECUTABLE=sincronizar_inscricoes_encontristas

# Cria o venv e instala dependências
install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

# Roda o código no ambiente virtual
run:
	$(VENV_PYTHON) $(MAIN_SCRIPT)

# Faz o build do executável e coloca na pasta dist/
deploy:
	@echo "Criando diretorio de distribuicao..."
	rm -rf $(DIST)
	mkdir -p $(DIST)

	@echo "Copiando arquivos essenciais..."
	cp .env $(DIST)/

	@echo "Gerando executável..."
	$(VENV_PYTHON) -m PyInstaller --onefile --name $(EXECUTABLE) $(MAIN_SCRIPT)

	@echo "Deploy criado em: $(DIST)/$(EXECUTABLE).exe"

# Remove os arquivos gerados pelo build
clean:
	rm -rf $(DIST) build __pycache__ *.spec
