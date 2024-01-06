FROM python:3.10-slim-bookworm

WORKDIR /backend

COPY ./pyproject.toml ./poetry.lock /backend/

RUN apt-get update
RUN apt-get -y install libpq-dev gcc

RUN pip install poetry

RUN poetry install

COPY . /backend/

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn --reload --host=0.0.0.0 --port=8000 app.main:app"]
