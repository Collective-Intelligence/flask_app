from flask_app import flask_app
from flask import Flask, render_template, url_for
from flask_app.config import Config
from celery import Celery
from flask_app import *


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


from flask_app import forms


@flask_app.route('/')
@flask_app.route('/index')
def index():
    user = {'username': 'Miguel'}
    var_thing = add.delay(10,10).wait()
    return render_template('index.html', title="title", user=user)


from flask import render_template, flash, redirect
@flask_app.route('/login', methods=['GET', 'POST'])
def login():

    form = forms.LoginForm()
    if form.validate_on_submit():

        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect("index")
    return render_template('login.html', title='Sign In', form=form)




