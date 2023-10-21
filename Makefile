ifdef PIPELINE
	RUN=python
else
	RUN=docker compose run --rm app
endif

run:
	docker compose up

up:
	docker compose up -d

lint:
	docker build -f Dockerfile --target test -t myapp-test .
	docker run --rm myapp-test \
		flake8 --exclude=*migrations*,*venv*,*__pycache__* .

safety:
	docker build -f Dockerfile --target test -t myapp-test .
	docker run --rm myapp-test \
		pip-audit -r /opt/requirements.txt

unit-test:
	docker build -f Dockerfile --target test -t myapp-test .
	docker run \
		-e DEBUG=True \
		-e DEVELOPMENT=True \
		-e LOG_LEVEL=DEBUG \
		-e OPENAI_KEY=xxx \
		-e GOOGLE_API_KEY=xxx \
		-e WHOAPI_KEY=xxx \
		--rm myapp-test \
		pytest /opt/tests

pre-commit: lint safety unit-test
