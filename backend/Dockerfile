FROM python:3.10-bookworm

WORKDIR /backend

COPY ./pyproject.toml ./poetry.lock /backend/

RUN pip install poetry

RUN poetry install

COPY . /backend/