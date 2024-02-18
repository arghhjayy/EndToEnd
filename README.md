# End to end ML Project

Project setup:

1. Open this in VSCode
2. Install [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
3. Do `Cmd + Shift + P` -> `Dev Containers: Rebuild Container Without Cache`
4. Activate the conda virtual environment: `source activate endtoend`
5. Inside Dev Container, run mlflow and prefect local servers: `nohup bash ./start_backend.sh`

## Model training:

Run: `python main.py`

## Model serving (deployment)

For batch inference, do the following:

1. Start the data generation worker process in a terminal instance: `make start_data_generator_worker`
2. Start the batch inference worker process in another terminal instance: `make start_batch_inference_worker`
3. Deploy the flows for #1 and #2: `prefect deploy --all`

If you want to run it for debugging, make sure you change the CRON expressions in `prefect.yaml`

## Tools used

- Pandas for data processing/engineering
- Sklearn for feature engineering and model development
- Pytest for testing
- MLFlow for experimentation tracking
- Prefect for workflow management(done) + orchestration (TBD)
- Black, isort and Flake8 for code styling and linting

## TODO list:

- :white_check_mark: Train and test flow
- :white_check_mark: Log metrics and artifacts to MLFlow
- :hourglass: Prefect for workflows
- :white_check_mark: Makefile
- :white_check_mark: Basic tests
- :hourglass: Model monitoring + scheduling it
- :soon: Containerization
- :soon: Use databases for input/output
- :soon: Feature store and vector store - TBD
- :soon: Streaming features
