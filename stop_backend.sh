prefect_pid="$(netstat -nlp | awk '$4~":'"4200"'"{ gsub(/\/.*/,"",$7); print $7 }')"
kill $prefect_pid
mlflow_pid="$(netstat -nlp | awk '$4~":'"5000"'"{ gsub(/\/.*/,"",$7); print $7 }')"
kill $mlflow_pid