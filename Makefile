build:
	docker build -t fqw .

run:
	docker run -p 80:5000 -d fqw

test:
	python3 tests/send_test_archive.py