FROM mcr.microsoft.com/devcontainers/miniconda:0-3

WORKDIR /workspaces/EndToEnd

ADD . /workspaces/EndToEnd

ENV PREFECT_API_URL=http://127.0.0.1:4200/api

RUN conda env create --file .devcontainer/environment.yaml && \
    echo "source activate endtoend" >> ~/.bashrc && \
    /bin/bash -c "source activate endtoend && cd .devcontainer && python -m pip install poetry==1.7.1 && python -m poetry install --no-root"

# To fix an mlflow bug which is to be fixed its next release
RUN sed -i 's/.get("mlflow\.app", \[\])/.select(group="mlflow.app")/' /opt/conda/envs/endtoend/lib/python3.12/site-packages/mlflow/cli.py

# make prefect available without sudo
RUN chmod 777 /opt/conda/envs/endtoend/lib/python3.12/site-packages/prefect/*

RUN chmod +x ./entrypoint.sh

EXPOSE 4200

EXPOSE 5000

ENTRYPOINT ["/workspaces/EndToEnd/entrypoint.sh"]
