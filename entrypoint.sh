#!/bin/bash

nohup ./start_backend.sh &
exec /opt/conda/envs/endtoend/bin/python main.py
