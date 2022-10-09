# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import input_required


# Author: William Newbould
# Form to create questions
class QuestionForm(FlaskForm):
    '''Takes in the FlaskForm library creating questions and validate them'''
    question = StringField(validators=[input_required()])
    option1 = StringField(validators=[input_required()])
    option2 = StringField(validators=[input_required()])
    option3 = StringField()
    option4 = StringField()
    answer = StringField(validators=[input_required()])
    submit = SubmitField()
