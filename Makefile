# Definições
PYTHON=python
VENV=venv
SRC=application\src
DIST=dist
MAIN_SCRIPT=$(SRC)\main.py  # Altere para o arquivo principal do seu projeto
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
	@echo "Criando diretorio de distribuicao..."
	if exist $(DIST) rmdir /s /q $(DIST)
	mkdir $(DIST)

	@echo "Copiando arquivos essenciais..."
	copy .env $(DIST)\

	@echo "Gerando executável..."
	pyinstaller --onefile --name $(EXECUTABLE) $(MAIN_SCRIPT) 

	@echo "Deploy criado em: $(DIST)\$(EXECUTABLE).exe"

# Remove os arquivos gerados pelo build
clean:
	rm -rf $(DIST) build __pycache__ *.spec

exit:
	deactivate
