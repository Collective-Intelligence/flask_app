from flask import Flask
from flask_app.config import Config
import socket
from celery import Celery
import json
import time


repo_dir = "/home/cuck/Desktop/Projects/flask_app/templates"
git_url = "https://github.com/Collective-Intelligence/website_start"

import shutil
import os
#shutil.rmtree(repo_dir)

#os.mkdir(repo_dir)



from git import Repo

#Repo.clone_from(git_url, repo_dir)



flask_app = Flask(__name__)
flask_app.config.from_object(Config)






TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

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
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(flask_app)


@celery.task
def login_celery(user_name,posting_key):
    print("here")
    # creates json to send to communication backend to create a session for the user, on login
    json_object = json.dumps({"action":"create_session", "key":posting_key,"steem-name":user_name, "system":"user","forward":"true"})
    return_info = send_json_account(json_object)
    return return_info




@celery.task
def buy_token(token,amount,user,key):
    json_object = json.dumps({"action":{"type":"account","action_type":"make_purchase","amount": amount,"token_type": token,"use-steem":"False"},"key":key,"steem-name":user, "system":"user", "forward":"true"})
    return send_json_account(json_object)


@celery.task
def create_curation_session(user,key,tag):
    json_object = json.dumps({"action":{"type":"create_session_curation", "tag":tag},"key":key,"steem-name":user, "forward":"false", "system":"curation"})
    return send_json_curation(json_object)

@celery.task
def get_session_list(user,key):
    json_object = json.dumps(
        {"action": {"type": "session"}, "key": key, "steem-name": user,"forward":"false","system":"curation"})
    return send_json_curation(json_object)

@celery.task
def add_post_curation(user,key,tag,post_link):
    json_object = json.dumps(
        {"action": {"type": "add_post", "tag": tag,"post-link":post_link}, "key": key, "steem-name": user, "forward":"true","system":"curation"})
    return send_json_curation(json_object)



@celery.task
def get_post_curation(user,key,tag):
    json_object = json.dumps(
        {"action": {"type": "get_post", "tag": tag}, "key": key, "steem-name": user, "forward":"true","system":"curation"})
    return send_json_curation(json_object)

@celery.task
def vote_post_curation(user,key,tag,vote,post_link):
    json_object = json.dumps(
        {"action": {"type": "add_vote", "tag": tag,"vote":[user,vote],"post":post_link}, "key": key, "steem-name": user, "forward":"true","system":"curation"})
    return send_json_curation(json_object)


def send_json_curation(MESSAGE):
    og = MESSAGE
    time_out = 300
    global  TCP_IP, BUFFER_SIZE
    TCP_PORT = 5001

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
        # waits until the task is done by the communication backend
        while not return_object or return_object == "404":
            data = ""
            times += 1
            if times > time_out:
                return False
            time.sleep(1)
            MESSAGE = json.dumps({"action": "return_json", "idnum": id})
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
    print(return_object)
    try:
        MESSAGE = json.loads(og)
        return_object = json.loads(return_object)
    except:
        pass
    has_error = True
    try:
        return_object["error"]
    except:
        has_error = False


    possible_info = ["post","tag_list"]
    info = ""
    for i in possible_info:
        try:
            print(i)
            return_object[i]
            print(return_object[i])
            if i == "post":
                print("here")
                info = "<info>" +return_object[i][0] + "</info>"
                print(return_object[i][0])
                break
            if i == "tag_list":
                info = "<info>" +json.dumps(return_object[i][0]) + "</info>"
        except Exception as e:
            print(e)
            pass

    if has_error:
        if type(MESSAGE["action"]) != str:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<error>" + str(return_object["error"]) + "</error>" \
                         "" + "<action>" + MESSAGE["action"]["type"] + "</action>" + info \
                         +"</data>"
        else:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<error>" + str(return_object["error"]) + "</error>" \
                           "" + "<action>" + MESSAGE["action"] + "</action>"  + info\
                                         +"</data>"

    else:
        if type(MESSAGE["action"]) != str:
            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<action>" + MESSAGE["action"]["type"]  + "</action>"  + info+ \
                                                                        "</data>"
        else:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<action>" +MESSAGE["action"] + "</action>" + info+\
                                                                "</data>"
    return xml_object


def send_json_account(MESSAGE):
    og = MESSAGE
    # takes json made by celery functions and sends it to the communication backend
    # then waits on the backend, checking in once a second, to get the return json
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
        # waits until the task is done by the communication backend
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
    try:
        MESSAGE = json.loads(og)
    except:
        pass
    try:
        print(return_object, type(return_object))
        return_object = json.loads(return_object)
    except:
        pass
    has_error = True
    try:
        return_object["error"]
    except:
        has_error = False

    possible_info = []
    info = ""
    for i in possible_info:
        try:
            return_object[i]

            break
        except:
            pass

    if has_error:
        if type(MESSAGE["action"]) != str:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<error>" + str(return_object["error"]) + "</error>" \
                                                                        "" + "<action>" + MESSAGE["action"][
                             "type"] + "</action>" + info \
                         + "</data>"
        else:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<error>" + str(return_object["error"]) + "</error>" \
                                                                        "" + "<action>" + MESSAGE[
                             "action"] + "</action>" + info \
                         + "</data>"

    else:
        if type(MESSAGE["action"]) != str:
            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<action>" + MESSAGE["action"]["type"] + "</action>" + info + \
                         "</data>"
        else:

            xml_object = "<data>" \
                         "" + "<success>" + str(return_object["success"]) + "</success>" + \
                         "" + "<action>" + MESSAGE["action"] + "</action>" + info + "</data>"

    return xml_object



from flask_app import routes
