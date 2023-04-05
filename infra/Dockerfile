FROM pulumi/pulumi

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
COPY ${PROJECT_PATH}/__main__.py ./
COPY ${PROJECT_PATH}/infra/ infra/

# Copy pulumi files
COPY ${PROJECT_PATH}/Pulumi.yaml ${PROJECT_PATH}/Pulumi.*.yaml ./

# Override entry point
ENTRYPOINT []
