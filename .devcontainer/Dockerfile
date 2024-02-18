FROM mcr.microsoft.com/devcontainers/miniconda:0-3

WORKDIR /workspaces/EndToEnd

COPY .devcontainer/environment.yaml /workspaces/EndToEnd/environment.yaml

COPY .devcontainer/poetry.lock /workspaces/EndToEnd/poetry.lock

COPY .devcontainer/pyproject.toml /workspaces/EndToEnd/pyproject.toml

RUN conda env create --file environment.yaml

SHELL ["conda", "run", "-n", "endtoend", "/bin/bash", "-c"]

RUN python -m pip install poetry==1.7.1

RUN poetry install --no-root

# To fix an mlflow bug which is to be fixed its next release
RUN sed -i 's/.get("mlflow\.app", \[\])/.select(group="mlflow.app")/' /opt/conda/envs/endtoend/lib/python3.12/site-packages/mlflow/cli.py

# make prefect available without sudo
RUN chmod 777 /opt/conda/envs/endtoend/lib/python3.12/site-packages/prefect/*

ENTRYPOINT ["source", "activate", "endtoend"]