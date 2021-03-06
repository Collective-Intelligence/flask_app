import flask_app
from flask import render_template, flash, redirect, url_for, request, make_response
import time
from flask import Response
from flask_app import forms
from flask_app import *
import os, random
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, form

from flask import send_from_directory

@flask_app.route('/', methods=['GET'])
@flask_app.route('/index', methods=['GET'])
def index():
    if not request.cookies.get('account'):

        return render_template('index.html', name=request.cookies.get('account'))
    else:
        return render_template('index.html', name=request.cookies.get('account'), active="True")


#@flask_app.route('/steem', methods=['GET', "POST"])
@flask_app.route('/login', methods=['GET', "POST"])
def login():
    form = forms.LoginForm()
    #form = forms.DepositForm()


    res = make_response(render_template('login.html', name="", form=form))
    if not request.cookies.get('session-key'):
        keys = get_keys()
        if keys:
            if keys["success"]:
                res = make_response(render_template('login.html', name="", form=form))

                res.set_cookie("session-key",keys["keys"][0], max_age=60 * 60 * 6)
                res.set_cookie("blockchain-key",keys["keys"][1], max_age=60 * 60 * 6)
                return res
        else:
            time.sleep(1)
            return redirect("/login")
        #res.set_cookie('account', "name", max_age=60*60*6)
    res = make_response(render_template('login.html', name=request.cookies.get("account"), form=form))




    if form.validate_on_submit():
        res = make_response(redirect("/index"))

        time.sleep(6)
        # checks if user key is correct
        res.set_cookie("account", form.username.data,  max_age=60 * 60 * 5.9)
        check_key_json = activate_key(form.username.data, request.cookies.get('session-key'))
        print("FORM VALID ON SUBMIT")
        print(check_key_json)
        if check_key_json:
            if check_key_json["success"]:
                res.set_cookie("active", "True",  max_age=60 * 60 * 5.9)
                return res
    #request.cookies.get('account')
    return render_template('login.html', name=request.cookies.get('account'), form=form)

@flask_app.route('/trending', methods=['GET'])
def trending():
    if not request.cookies.get('account'):

        return render_template('trending.html', name=request.cookies.get('account'))
    else:
        return render_template('trending.html', name=request.cookies.get('account'), active="True")



@flask_app.route('/shop', methods=['GET'])
def shop():
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
    return render_template('shop.html', name=request.cookies.get('account'), MESSAGE="", active="True")

@flask_app.route('/steem', methods=['GET', "POST"])
def steem():
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
    form = forms.DepositForm()
    if form.validate_on_submit():
        time.sleep(6)
     #   return render_template('steem.html', name=request.cookies.get('account'), form=form)

    return render_template('steem.html', name=request.cookies.get('account'), form=form, active="true")

@flask_app.route('/main.css', methods=['GET'])
def maincss():
    return send_from_directory("static",
                               "main.css")
@flask_app.route('/markdown.js', methods=['GET'])
def markdown():
    return send_from_directory("static",
                               "markdown.js")

@flask_app.route('/memos.js', methods=['GET'])
def memos():
    return send_from_directory("static",
                               "memos.js")


@flask_app.route('/getAccount.js', methods=['GET'])
def getaccount():
    return send_from_directory("static",
                               "getAccount.js")

@flask_app.route('/logo.png', methods=['GET'])
def logopng():
    return send_from_directory("static",
                               "logo.png")



@flask_app.route('/login_old', methods=["GET",'POST'])
def login_old():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
   # info = request.get_json(force=True)
 #   print("HEADERS", request.headers)
#    print("REQ_path", request.path)

 #   print("ARGS", request.args)
#    print("DATA", request.data)

    #print("FORM", request.form)
    #print("DIR", dir(request."titleform))
    #print("GETLIST", request.form.items())
    #print("LAST THING", request.form.getlist("password")[0])
        password = form.username.data
        username = form.password.data
    #form = forms.LoginForm()

    #print(form.username)
    #print("Here")
        if True:
            print("here2")
        #login_celery.delay(form.username.data,form.password.data).wait()
            #xml_res = login_celery.delay(username,password).wait()






            #return Response(xml_res, mimetype='text/xml')


    return render_template("login.html",form=form,name=request.cookies.get('account'))







@flask_app.route('/create_curation', methods=['POST'])
def create_curation():
    return
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]
    tag = request.form.getlist("tag")[0]
    xml_res = create_curation_session(username, password, tag)

    return Response(xml_res, mimetype='text/xml')

@flask_app.route("/add_post_curation/<int:message_number>", methods=["GET", "POST"])
def add_post_curation(message_number):
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
        account = request.cookies.get("account")



    print(type(message_number))
    form = forms.submit_post()
    if message_number == 0:
        message = "The system you tried to access is out of posts, you will have to submit one."
    elif message_number == 1:
        message = "Post has been Submitted, would you like to submit another?"
    elif message_number == 2:
        message = "There was an error submitting the post"
    else:
        message = "Submit a post to the curation system"
    if form.validate_on_submit():

        password = key
        username = account
        tag = form.action.data
        print(tag)
        post_link = request.form.getlist("post_link")[0]



        success = add_post_curation_celery(username, password,tag,post_link)

        if success and success["success"]:
            return render_template("add_post.html", name=request.cookies.get('account'),form=form, MESSAGE="Post submitted",steps="../", active="true")
        else:
            if success and success["error"] == 1002:
                return render_template("add_post.html", name=request.cookies.get('account'), form=form,
                                       MESSAGE="Post did not submit, two posts by the same author are not allowed (or maybe it just glitched, who knows).", steps="../",active="true")

            return render_template("add_post.html", name=request.cookies.get('account'),form=form, MESSAGE="Post did not submit, are you sure you have enough tokens?", steps="../",active="true")


    return render_template("add_post.html",name=request.cookies.get('account'), form=form, MESSAGE=message, steps="../",active="true")

    pass


@flask_app.route('/curation', methods=["GET", "POST"])
def curation():
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
        account = request.cookies.get("account")

    with forms.get_post.locks["update"]:
        form = forms.get_post()
        if random.randrange(100) > 98:
            update_form()
    print("HERE")

    #print(form.update())

    if form.validate_on_submit():
        username = account
        password = key

        post_url = get_post_curation(username, password, form.action.data)
        #flash('getting post {}'.format(
         #   form.username.data))
        print("START")
        if post_url:
            print("RETURN EXISTS")
            if post_url["success"] == True:
                print("Worked")
                post_url = post_url["post"]
                new_url = ""
                for i in post_url[0]:
                    if i =="/":
                        new_url += "|"
                    else:
                        new_url += i
                return redirect("/vote_post/" + new_url + "/" + form.action.data)
            else:

                return redirect("/add_post_curation/0")
        print("THIS THING")
    print("END HERE")


    return render_template("curation.html",name=request.cookies.get('account'), form=form,active="true")

def update_form():

    object = get_session_list()
    buttons = []
    for i in range(len(object["tag_list"])):
        buttons.append((i,object["tag_list"][i]))
    forms.get_post.buttons = buttons
    forms.get_post.action = RadioField(label='Which system do you want to rate a post from?',
                                       choices=forms.get_post.buttons)

    pass

@flask_app.route('/vote_post/<string:post_name>/<string:tag>', methods=["GET","POST"])
def vote_post(post_name,tag):
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
        account = request.cookies.get("account")

    print("STARTING VOTE POST")
    new_post_name = ""
    for i in post_name:
        if i == "|":
            new_post_name += "/"
        else:
            new_post_name += i
    post_name = new_post_name
    form = forms.vote_post()

    if form.validate_on_submit():
        password = key
        username = account
        vote = int(form.action.data)
        post_link = post_name

        worked = vote_post_curation(username, password,tag, vote, post_link)
        if not worked or worked["success"] == False:
            render_template("vote_post.html",name=request.cookies.get('account'), form=form, MESSAGE = "VOTE ERROR, please try again: What do you think of: " + post_name, steps="../../", active="true")
        else:
            return redirect("/curation")
    return render_template("vote_post.html",name=request.cookies.get('account'), form=form, MESSAGE = "What do you think of: " + post_name, steps="../../", active="true")

    pass




















@flask_app.route('/add_post', methods=['POST'])
def add_post():
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]
    tag = request.form.getlist("tag")[0]
    post_link = request.form.getlist("post-link")[0]
    xml_res = add_post_curation(username, password, tag, post_link)

    return Response(xml_res, mimetype='text/xml')



@flask_app.route('/vote_post1', methods=['POST'])
def vote_post1():
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]
    tag = request.form.getlist("tag")[0]
    post_link = request.form.getlist("post-link")[0]
    vote = int(request.form.getlist("vote")[0])

    xml_res = vote_post_curation(username, password, tag, vote,post_link)

    return Response(xml_res, mimetype='text/xml')


@flask_app.route('/get_session_list', methods=['POST'])
def get_session_lists():
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]


    xml_res = get_session_list(username, password)

    return Response(xml_res, mimetype='text/xml')


@flask_app.route("/logout", methods=["GET"])
def logout():
    cookie_list = ["active", "session-key", "blockchain-key", "account"]
    delete_key(request.cookies.get('account'),request.cookies.get('session-key'))
    resp = make_response(redirect("/login"))

    for i in cookie_list:
        try:
            resp.set_cookie(i, '', expires=0)
        except:
            pass

    return resp

@flask_app.route('/buy_token', methods=['POST'])
def buy_tokens():
    if not request.cookies.get('active'):
        return redirect("/login")
    else:
        key = request.cookies.get("session-key")
        account = request.cookies.get("account")

    #print(request.form.getlist("token"))

    password = key
    username = account
    token = request.form.getlist("token")[0]
    amount = int(request.form.getlist("amount")[0])
    xml_res = buy_token(token, amount, username, password, False)

    #xml_res = "<info></info>"

    #return Response(xml_res, mimetype='text/xml')
    if xml_res:
        if xml_res["success"] == True:
            return render_template("shop.html",name=request.cookies.get('account'), MESSAGE = "Purchase successful")

        elif xml_res["error"] == 10991:
            return redirect("/login")
        elif xml_res["error"] == 10992:
            return render_template("shop.html",name=request.cookies.get('account'), MESSAGE = "Steem connection error")



    return render_template("shop.html",name=request.cookies.get('account'), MESSAGE = "Connection error")




@flask_app.route('/get_post', methods=['POST'])
def get_post():
    password = request.form.getlist("password")[0]
    username = request.form.getlist("username")[0]
    amount = int(request.form.getlist("amount")[0])
    xml_res = get_post(token,amount,username, password, True)

    return Response(xml_res, mimetype='text/xml')