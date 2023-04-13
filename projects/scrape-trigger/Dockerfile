FROM python:3.9.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJECT_PATH

WORKDIR /app

# Install docker compose wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

# Download AWS runtime interface emulator
RUN curl -Lo /usr/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x /usr/bin/aws-lambda-rie

# Install python requirements
RUN pip install poetry \
    && poetry config virtualenvs.create false

# Install package dependencies
COPY ${PROJECT_PATH}/poetry.lock ${PROJECT_PATH}/pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Mount package
COPY ${PROJECT_PATH}/scrape_trigger/ scrape_trigger/

# Copy entrypoint script
COPY scripts/aws-lambda-entrypoint.sh aws-lambda-entrypoint.sh
RUN chmod +x aws-lambda-entrypoint.sh

# Set entrypoint
WORKDIR /app/scrape_trigger
ENTRYPOINT [ "/app/aws-lambda-entrypoint.sh" ]
CMD [ "main.run" ]
