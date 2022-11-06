FROM python:3.9.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJECT_PATH

WORKDIR /app

# Install python requirements
RUN pip install poetry \
    && poetry config virtualenvs.create false

# Install package dependencies
COPY ${PROJECT_PATH}/poetry.lock ${PROJECT_PATH}/pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Mount package
COPY ${PROJECT_PATH}/infra/ infra/
