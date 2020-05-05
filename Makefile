.PHONY: requirements create_environment

PYTHON_INTERPRETER="python3"
PROJECT_NAME="repository_mining"

requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

create_environment:
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv
	@echo ">>> Installing virtualenvwrapper if not already installed.\n"
	virtualenv env
	@echo ">>> Creating virtualenv.\n"
