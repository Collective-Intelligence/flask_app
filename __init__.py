from flask import Flask, render_template, url_for
from flask_app.config import Config
from celery import Celery
from flask_app.forms import LoginForm
var_thing = 10

flask_app = Flask(__name__)
flask_app.config.from_object(Config)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
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


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)

#objthing = object_thing.TestObj()
@celery.task
def add(x, y):
    global var_thing
    print(var_thing)
    return x + y + var_thing


from flask_app import routes

