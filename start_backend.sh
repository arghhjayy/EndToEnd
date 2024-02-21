#!/bin/bash

/opt/conda/envs/endtoend/bin/mlflow server --host 0.0.0.0 &
/opt/conda/envs/endtoend/bin/prefect server start --host 0.0.0.0 &