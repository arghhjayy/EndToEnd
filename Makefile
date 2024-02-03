test:
	pytest tests/
# run the pipeline, end to end
run:
	python main.py
run_prefect:
	prefect server start
run_mlflow:
	mlflow server