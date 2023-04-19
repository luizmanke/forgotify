FROM python:3.9.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJECT_PATH

WORKDIR /app

# Install docker compose wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

# Install python requirements
RUN pip install poetry \
    && poetry config virtualenvs.create false

# Install package dependencies
COPY ${PROJECT_PATH}/poetry.lock ${PROJECT_PATH}/pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Mount package
COPY ${PROJECT_PATH}/cloud_tools/ cloud_tools/
