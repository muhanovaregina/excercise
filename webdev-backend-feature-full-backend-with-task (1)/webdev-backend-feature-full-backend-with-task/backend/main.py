# -*- coding: utf-8 -*-

DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID

from time import sleep

from celery import Celery
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
app.config.update({
    'CELERY_BACKEND': 'mongodb://localhost/celery',
    'CELERY_BROKER_URL': 'amqp://guest:guest@localhost:5672//'
})


def make_celery(app):
    celery = Celery('backend.main', backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)


@celery.task
def long_running_job(click_count):
    sleep(5)
    return click_count ** 3


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def data():
    click_count = int(request.args.get('cc', 0))
    task_id = long_running_job.delay(click_count)

    return jsonify({
        'count': click_count,
        'squared': click_count ** 2,
        'task_id': str(task_id)
    })


@app.route('/result/<task_id>')
def result(task_id):
    async_result = celery.AsyncResult(task_id)

    return jsonify({
        'ready': async_result.ready(),
        'status': async_result.status,
        'result': async_result.result,
        'task_id': str(async_result.task_id)
    })


if __name__ == '__main__':
    app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
