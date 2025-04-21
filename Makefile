requirements-linux:
	@pip install -r requirements.txt
	@sudo apt install -y python3-tk

requirements-windows:
	@pip install -r requirements.txt