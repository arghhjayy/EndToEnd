start_all_prefect_workers: start_data_generator_worker start_batch_inference_worker start_model_monitor_worker 
test:
	TESTING=TRUE pytest tests/
# run the pipeline, end to end
run:
	python main.py
run_prefect_server:
	prefect server start &
run_mlflow_server:
	mlflow server &
start_data_generator_worker:
	prefect work-pool create --type process data-generator-work-pool
	nohup prefect worker start --pool data-generator-work-pool &
start_batch_inference_worker:
	prefect work-pool create --type process batch-inference-work-pool
	nohup prefect worker start --pool batch-inference-work-pool &
start_model_monitor_worker:
	prefect work-pool create --type process model-monitor-work-pool
	nohup prefect worker start --pool model-monitor-work-pool &