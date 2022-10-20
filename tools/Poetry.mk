poetry-lock:
	poetry lock

poetry-reinstall:
	rm -rf $(shell poetry env info -p)
	poetry shell
	poetry install
