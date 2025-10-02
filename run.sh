#!/bin/bash

# truncate logs file
> logs.txt

# activate virtual environment
source .venv/bin/activate

# start Uvicorn in background and redirect logs
uvicorn src.main:app --reload > logs.txt 2>&1 &

# print message with PID
echo "Uvicorn started in background with PID $!"
echo "Logs are being written to logs.txt"

