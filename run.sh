#!/bin/bash -e

echo "Starting script: $0"

if [ $# != 1 ]; then
  echo "Warning: No input path detected. Defaulting to ./tmp directory to search for input file."
fi

export PYTHONPATH='.'

echo "Running PIP Install for Luigi"
pip install -r ./code/requirements.txt
echo "Running Luigi Pipeline for file: $1"
luigi --module code.TfIdfPipeline rubrikloud.TfIdfPipeline --local-scheduler --input-path "$1"
