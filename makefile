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
	# mysql -u yusuk -p -e "DROP DATABASE IF EXISTS ShiftBot"
	# mysql -u yusuk -p -e "CREATE DATABASE ShiftBot"
	mysql -u yusuk -p ShiftBot < static/sql/init.sql
	mysql -u yusuk -p ShiftBot < static/sql/data/insert.sql
