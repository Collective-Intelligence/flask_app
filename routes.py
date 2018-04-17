from flask_app import flask_app
from flask import render_template, flash, redirect
from flask_app import forms
from flask_app import *
@flask_app.route('/')
@flask_app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)




@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    print("Here")
    if form.validate():
        print("here2")
        #login_celery.delay(form.username.data,form.password.data).wait()
        token_thing = create_curation_session.delay(form.username.data,form.password.data,"tag").wait()
        #time.sleep(5)
        #t#oken_thing = add_post_curation.delay(form.username.data,form.password.data,"tag","post-link").wait()


        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        print("here")
        return redirect("/index")


    return render_template('login.html', title='Sign In', form=form)