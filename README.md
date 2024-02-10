# End to end ML Project

Project setup:

1. Download and install Anaconda: https://www.anaconda.com/download
2. Setup a virtual env using conda cli: `conda env create -f environment.yml`
3. Activate the env: `conda activate endtoend`
4. Install `poetry`: `python -m pip install poetry`
5. Install all dependencies using `poetry` cli: `poetry install --no-root`
6. Run the mlflow server: `mlflow server`, run the prefect server: `prefect server start`

## Model training:

Run: `python main.py`

**Note**: To make it work, we need to do a quick hack:<br>
in `<condaenvname>/lib/python3.12/importlib/metadata/__init__.py/`,
add a method `get()` to the class `EntryPoints(tuple)`:

```python
def get(self, name, default):
    try:
        return self.__getitem__(name)
    except Exception:
        return default
```

in Windows conda, the location of the file most likely is:
<br>
`C:\Users\<YourUserName>\anaconda3\envs\<condaenvname>\Lib\importlib\metadata\__init__.py`

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
- :soon: Model monitoring + scheduling it
- :soon: Containerization
- :soon: Use databases for input/output
- :soon: Feature store and vector store - TBD
- :soon: Streaming features
