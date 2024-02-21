#!/bin/bash

nohup ./start_backend.sh &

check_process() {
    port=$1
    pid=$(lsof -t -i :$port)
    echo $pid
}

while true; do
    # Check for both processes
    pid_4200=$(check_process 4200)
    pid_5000=$(check_process 5000)

    if [ -z "$pid_4200" ] || [ -z "$pid_5000" ]; then
        echo "Processes not found on one or both ports. Waiting..."
        sleep 1
    else
        echo "Processes found on both ports. Starting main.py."
        exec /opt/conda/envs/endtoend/bin/python main.py
        break
    fi
done