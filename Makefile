install:
	( \
	  virtualenv -p python3 env; \
	  source env/bin/activate; \
	  pip3 install -r requirements.txt; \
	)
run:
	( \
	  source env/bin/activate; \
	  python3 bot.py; \
	)
