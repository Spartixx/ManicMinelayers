up:
	docker compose run --rm app python3 -m src.cli.main human stupidbot

build:
	docker compose build app
