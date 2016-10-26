# WebDev Backend

## Installation

```
virtualenv venv --python=python3
. venv/bin/activate
pip install -r requirements.txt
```

## Running celery worker

Requires RabbitMQ and MongoDB to be up and running.

```
. venv/bin/activate
celery -A backend.main.celery worker -l info
```

## Running web application

```
. venv/bin/activate
python -m backend.main
```
