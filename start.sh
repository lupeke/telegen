#!/usr/bin/env bash

set -Eeuo pipefail

python ./chatbot.py &

if [ "$ENV" = "dev" ]; then
    flask --app webpage run --host=0.0.0.0 --debug &
else
    gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 webpage:app &
fi

wait -n
