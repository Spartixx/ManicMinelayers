up:
	docker compose run --rm app python3 -m src.cli.main human stupid_bot --ai_speed 0

build:
	docker compose build app
