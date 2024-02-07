test:
	pytest tests/
# run the pipeline, end to end
run:
	python main.py
run_prefect_server:
	prefect server start
run_mlflow_server:
	mlflow server
start_data_generator_worker:
	prefect work-pool create --type process data-generator-work-pool
	prefect worker start --pool data-generator-work-pool
start_batch_inference_worker:
	prefect work-pool create --type process batch-inference-work-pool
	prefect worker start --pool batch-inference-work-pool &