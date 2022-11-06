FROM python:3.9.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJECT_PATH

WORKDIR /app

# Install python requirements
RUN pip install poetry \
    && poetry config virtualenvs.create false

# Copy local libs
COPY libs/ /libs/

# Copy local projects
COPY projects/ /projects/

# Install package dependencies
COPY ${PROJECT_PATH}/poetry.lock ${PROJECT_PATH}/pyproject.toml ./
RUN poetry install --no-root --no-interaction --no-ansi

# Mount package
COPY ${PROJECT_PATH}/pipelines/ pipelines/

# Remove local libs
RUN rm -rf /libs

# Remove local projects
RUN rm -rf /projects

# Copy dagit workspace
COPY ${PROJECT_PATH}/workspace.yaml ./
