from flask import Flask, render_template, url_for
from flask_app.config import Config
from celery import Celery
from flask_app.forms import LoginForm
import json
var_thing = 10


import socket
import threading
import time
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

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
def login(user_name,posting_key):
    json_object = json.dumps({"action":"create_session", "key":posting_key,"steem-name":user_name})

    print(1)
    return send_json(json_object)

def send_json(MESSAGE):
    time_out = 300
    global TCP_PORT, TCP_IP, BUFFER_SIZE
    return_object = False
    print(2)
    try:


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE.encode())
        data = ""
        print(3)
        while True:
            new_data = s.recv(BUFFER_SIZE)
            new_data = new_data.decode()
            data += new_data
            if not new_data: break
            if not len(new_data) > 0: break
            if not len(new_data) > BUFFER_SIZE: break
        id = json.loads(data)["idnum"]
        data = ""
        times = 0
        while not return_object or return_object == "404":
            data = ""
            times +=1
            if times > time_out:
                return False
            time.sleep(1)
            MESSAGE = json.dumps({"action":"return_json","idnum":id})
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(MESSAGE.encode())
            while True:
                new_data = s.recv(BUFFER_SIZE)
                new_data = new_data.decode()
                data += new_data
                if not new_data: break
                if not len(new_data) > 0: break
                if not len(new_data) > BUFFER_SIZE: break

            if data != "":
                return_object = data


    except Exception as e:
        print(e)
        pass

    return return_object


from flask_app import routes

