test:
	pytest tests/
# run the pipeline, end to end
run:
	python main.py
run_prefect_server:
	prefect server start
run_mlflow_server:
	mlflow server
setup_prefect:
	prefect work-pool create data-generator
	prefect worker start --pool 'data-generator'
	prefect deploy