from flask_app import flask_app
from flask import render_template, flash, redirect, url_for, request
from flask import Response
from flask_app import forms
from flask_app import *
import os
@flask_app.route('/')
@flask_app.route('/index')
def index():
    form = forms.LoginForm()

    #return flask_app.send_static_file("index.html")

    return render_template("index.html",form=form)

@flask_app.route('/login', methods=['POST'])
def login():
   # info = request.get_json(force=True)
 #   print("HEADERS", request.headers)
#    print("REQ_path", request.path)

 #   print("ARGS", request.args)
#    print("DATA", request.data)

    #print("FORM", request.form)
    #print("DIR", dir(request.form))
    #print("GETLIST", request.form.items())
    #print("LAST THING", request.form.getlist("password")[0])
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]
    #form = forms.LoginForm()

    #print(form.username)
    #print("Here")
    if True:
        print("here2")
        #login_celery.delay(form.username.data,form.password.data).wait()
        xml_res = login_celery.delay(username,password).wait()
        print(xml_res)
        #time.sleep(5)
        #t#oken_thing = add_post_curation.delay(form.username.data,form.password.data,"tag","post-link").wait()




        print("here")


        return Response(xml_res, mimetype='text/xml')


    return redirect("/")