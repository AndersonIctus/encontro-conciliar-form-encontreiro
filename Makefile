# Definições
PYTHON=python
VENV=venv
SRC=applications/src
DIST=dist
MAIN_SCRIPT=$(SRC)/main.py  # Altere para o arquivo principal do seu projeto
EXECUTABLE=sincronizar_inscricoes_encontristas  # Nome do executável final

#	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted
# Ativa o venv e instala dependências
install:
	$(PYTHON) -m venv $(VENV)
	.\$(VENV)\Scripts\activate && pip install -r requirements.txt

# Roda o código no ambiente virtual
run:
	$(VENV)/Scripts/activate && $(PYTHON) $(MAIN_SCRIPT)

# Faz o build do executável e coloca na pasta dist/
deploy:
	rm -rf $(DIST)
	mkdir -p $(DIST)
	pyinstaller --onefile --name $(EXECUTABLE) --distpath $(DIST) $(MAIN_SCRIPT)

# Remove os arquivos gerados pelo build
clean:
	rm -rf $(DIST) build __pycache__ *.spec

exit:
	deactivate
