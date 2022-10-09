import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import input_required, Email, Length, EqualTo, ValidationError


def character_check(form, field):
    '''Checks the fields and preventing them of having specific characters in them.'''
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class LoginForm(FlaskForm):
    '''Checks and submits login form for the user'''
    username = StringField(validators=[input_required()])
    password = PasswordField(validators=[input_required()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    '''Checks and submits register form for the user'''
    firstname = StringField(validators=[input_required(), character_check])
    lastname = StringField(validators=[input_required(), character_check])
    username = StringField(validators=[input_required()])
    email = StringField(validators=[input_required(), Email()])

    # Function to validate the password.
    def validate_password(self, password):
        '''Takes the password and checks for minimum requirements that we have set.'''
        pattern = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d])')
        if not pattern.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit,"
                                  " 1 lowercase, 1 uppercase and 1 special "
                                  "character.")

    password = PasswordField(validators=[input_required(),
                                         Length(min=8, max=15,
                                                message='Password must be between 8 and 15 '
                                                        'characters in length.')])
    confirm_password = PasswordField(
        validators=[input_required(),
                    EqualTo('password',
                            message='Both password fields must be equal!')])

    submit = SubmitField()


# Author: William Newbould
# Form to create message
class MessageForm(FlaskForm):
    sender = StringField()
    receiver = StringField(validators=[input_required()])
    header = StringField(validators=[input_required()])
    body = StringField(validators=[input_required()])
    send = SubmitField()
