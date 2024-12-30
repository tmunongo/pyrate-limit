# Rate Limiting strategies

A repo for a blog post on API rate limiting strategies with the full Python code examples using FastAPI

## Clone the repo

`git clone https://github.com/tmunongo/pyrate-limit.git`

## Create a virtual environment (optional)

`python3 -m venv venv`

## Activate venv

`source venv/bin/activate`

## Install dependencies

`pip install -r requirements.txt`

## Run

`fastapi dev token-bucket.py`

# For Redis

## Start containers

`docker compose up --build`

## Use the test script

`python3 test/test_distributed.py`
