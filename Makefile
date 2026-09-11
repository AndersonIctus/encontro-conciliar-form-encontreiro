# Definições
VENV=.venv
SRC=application/src
DIST=dist
MAIN_SCRIPT=$(SRC)/main.py
EXECUTABLE=sincronizar_inscricoes_encontristas

# Cria o venv e instala dependências com uv
install:
	uv venv $(VENV)
	uv pip install -r requirements.txt

# Roda o código no ambiente virtual
run:
	uv run $(MAIN_SCRIPT)

# Faz o build do executável e coloca na pasta dist/
deploy:
	@echo "Criando diretorio de distribuicao..."
	rm -rf $(DIST)
	mkdir -p $(DIST)

	@echo "Copiando arquivos essenciais..."
	cp .env $(DIST)/

	@echo "Gerando executável..."
	uv run pyinstaller --onefile --name $(EXECUTABLE) $(MAIN_SCRIPT)

	@echo "Deploy criado em: $(DIST)/$(EXECUTABLE).exe"

# Remove os arquivos gerados pelo build
clean:
	rm -rf $(DIST) build __pycache__ *.spec
