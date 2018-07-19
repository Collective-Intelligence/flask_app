from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, form
from wtforms.validators import DataRequired
from flask_app import *
import time
import threading

curation_systems = [("TAG","TAG")]
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    pass


class get_post(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    last_check_time = time.time()
    print("DOING GET SESSION LIST")
    print("HERE")
#    object = get_session_list.delay().wait()
    global curation_systems
    buttons = curation_systems
    #for i in range(len(object["tag_list"])):
     #   buttons.append((i,object["tag_list"][i]))
    action = RadioField(label='Which system do you want to rate a post from?',choices=buttons)
    locks = {"update":threading.Lock(), "time":threading.Lock()}


    submit = SubmitField('Sign In')
#    def update(self):
 #       self.action = RadioField(label='Which system do you want to rate a post from?', choices=self.buttons)
      #  pass

class vote_post(FlaskForm):
    actions = [
        ('-1', 'Bad post'),
        ('0', 'Average post'),
        ('1', 'Good Post'),
        ("get_post", 'Get Post'),
    ]
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    action = RadioField(label='What is your opinion on the post?',choices=actions)
    submit = SubmitField('Sign In')



class submit_post(FlaskForm):



    global curation_systems
    actions = curation_systems
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    post_link = StringField('Post Link', validators=[DataRequired()])

    action = RadioField(label='What system do you want to add a post to?',choices=actions)
    submit = SubmitField('Sign In')