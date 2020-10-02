.PHONY: bhaga
bhaga:
	mkdir bhaga
	cp -r plugins/bhaga bhaga/
	cp pyproject.toml bhaga/
	cp poetry.lock bhaga/
	cp *.ini bhaga/
	cp run.py bhaga/
	cp slackbot_srttings.py bhaga/
	cd bhaga
	poetry install
	poetry shell
	python run.py

shiftbot:
	mkdir shiftbot
	cp -r plugins/shiftbot shiftbot/
	cp pyproject.toml shiftbot/
	cp poetry.lock shiftbot/
	cp *.ini shiftbot/
	cp run.py shiftbot/
	# TODO: use contexual file
	cp slackbot_srttings.py shiftbot/
	cd shiftbot
	poetry install
	poetry shell
	python run.py

.PHONY: init
init:
	mysql -u root -p -e "DROP DATABASE IF EXISTS bhaga"
	mysql -u root -p -e "CREATE DATABASE bhaga"
	mysql -u root -p bhaga < static/sql/init.sql
	mysql -u root -p bhaga < static/sql/data/insert.sql
