from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, form, IntegerField
from wtforms.validators import DataRequired
#from flask_app import *
import time
import threading

curation_systems = [("STEM","STEM"), ("LGBT","LGBT"), ("humor","humor"), ("politics/economics","politics/economics")
                    , ("art","art"), ("blog/writing","blog/writing"), ("TIL","TIL"), ("news", "news")]
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Sign In')


class DepositForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])

    submit = SubmitField('Send Steem')


class get_post(FlaskForm):
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


    submit = SubmitField('Get post')
#    def update(self):
 #       self.action = RadioField(label='Which system do you want to rate a post from?', choices=self.buttons)
      #  pass

class vote_post(FlaskForm):
    actions = [
        ('-1', 'Bad post'),
        ('0', 'Average post'),
        ('1', 'Good Post'),
    ]
    action = RadioField(label='What is your opinion on the post?',choices=actions)
    submit = SubmitField('Vote post')



class submit_post(FlaskForm):



    global curation_systems
    actions = curation_systems
    post_link = StringField('Post Link', validators=[DataRequired()])

    action = RadioField(label='What system do you want to add a post to?',choices=actions)
    submit = SubmitField('Submit post')