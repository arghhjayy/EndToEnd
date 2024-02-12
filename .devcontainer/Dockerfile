FROM mcr.microsoft.com/devcontainers/miniconda:0-3

WORKDIR /workspaces/EndToEnd

COPY .devcontainer/environment.yaml /workspaces/EndToEnd/environment.yaml

COPY .devcontainer/poetry.lock /workspaces/EndToEnd/poetry.lock

COPY .devcontainer/pyproject.toml /workspaces/EndToEnd/pyproject.toml

RUN conda env create --file environment.yaml

SHELL ["conda", "run", "-n", "endtoend", "/bin/bash", "-c"]

RUN python -m pip install poetry==1.7.1

RUN poetry install --no-root

ENTRYPOINT ["conda", "activate", "endtoend"]