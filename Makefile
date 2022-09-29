build:
	docker-compose build

run:
	docker-compose up

app_down:
	docker-compose down

test:
	python3 tests/send_test_archive.py