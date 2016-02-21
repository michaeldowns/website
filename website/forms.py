from flask.ext.wtf import Form, RecaptchaField
from wtforms.fields import (
    TextField, PasswordField, SubmitField, BooleanField, TextAreaField,
    IntegerField)
from wtforms.validators import Required, Email, EqualTo, Length, Regexp

from . import app
from .util.validators import *
from .models import User


class ProblemForm(Form):
    answer = TextField("Answer", validators=[Required()])

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")

    
class RegisterForm(Form):
    email = TextField("Email", validators=[
        Required(message="You must enter an email"),
        Email(),
        Unique(
            User,
            User.email,
            message="There is already an account with that email"
        )
    ])

    username = TextField("Username", validators=[
        Required(message="You must enter a username"),
        Length(min=4, max=25,
               message="Your username must be between 4 to 25 characters"),
        Regexp('^[A-za-z][A-za-z0-9_]*$',
               0,
               "Usernames must start with a letter and contain only letters, underscores, and numbers"
        ),
        Unique(
            User,
            User.username,
            message="There is already an account with that username"
        )
    ])
    password = PasswordField("Password", validators=[
        Required(message="You must enter a password"),
        Length(min=8,
               message="Your password must be at least 8 characters long")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        Required(message="You must confirm your password"),
        EqualTo("password", message="Passwords do not match")
    ])

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")

    
class LoginForm(Form):
    username = TextField("Username", validators=[
        Required(message="You must enter a username"),
        Exists(
            User,
            User.username,
            message="Username does not exist"
        ),
        Active(),
        EmailConfirmed()
    ])

    password = PasswordField("Password", validators=[
        Required(message="You must enter a password."),
        CorrectPassword()
    ])

    remember_me = BooleanField("Keep me logged in")

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")

    
class EmailForm(Form):
    email = TextField("Email", validators=[
        Required(message="You must enter an email."),
        Email()
    ])

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")


class PasswordForm(Form):
    password = PasswordField("Password", validators=[
        Required(message="You must enter a password."),
        Length(min=8,
               message="Your password must be at least 8 characters long")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        Required(message="You must confirm your password"),
        EqualTo("password", message="Passwords do not match")
    ])

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")

    
class ChangePasswordForm(Form):
    current_password = PasswordField("Current Password", validators=[
        Required(message="You must enter your current password."),
        CorrectPasswordAuthed()
    ])
    
    new_password = PasswordField("New Password", validators=[
        Required(message="You must enter a password."),
        Length(min=8,
               message="Your password must be at least 8 characters long")
    ])
    
    confirm_new_password = PasswordField("Confirm New Password", validators=[
        Required(message="You must confirm your password"),
        EqualTo("new_password", message="Passwords do not match")
    ])

    submit = SubmitField("Submit")

    
class ChangeEmailForm(Form):
    email = TextField("Email", validators=[
        Required(message="You must enter an email."),
        Email()
    ])
    
    password = PasswordField("Password", validators=[
        Required(message="You must enter your current password."),
        CorrectPasswordAuthed()
    ])

    submit = SubmitField("Submit")

    
class NewsPostForm(Form):
    title = TextField("Title", validators=[
        Required(message="You must enter a title.")
    ])

    text = TextAreaField("Body", validators=[
        Required(message="You must enter a body.")
    ])

    submit = SubmitField("Submit")


class EditNewsPostForm(NewsPostForm):
    delete = BooleanField("Delete Post")

    submit = SubmitField("Submit")
    

class EditUserForm(Form):
    email = TextField("Email", validators=[
        Required(message="You must enter an email"),
        Email()
    ])
    
    username = TextField("Username", validators=[
        Required(message="You must enter a username"),
        Length(min=4, max=25,
               message="Your username must be between 4 to 25 characters"),
        Regexp('^[A-za-z][A-za-z0-9_]*$',
               0,
               "Usernames must start with a letter and contain only letters, underscores, and numbers"
        )
    ])

    password = PasswordField("Password")
    
    email_confirmed = BooleanField("Email confirmed")

    moderator = BooleanField("Is moderator")

    delete_user = BooleanField("Delete user")

    submit = SubmitField("Submit")


class EditProblemForm(Form):
    title = TextField("Title", validators=[
        Required(message="You must enter a title.")
    ])

    text = TextAreaField("Body", validators=[
        Required(message="You must enter a body.")
    ])

    difficulty = IntegerField("Difficulty", validators=[
        Required(message="You must enter a difficulty.")
    ])

    solution = TextField("Solution", validators=[
        Required(message="You must enter a solution.")
    ])


    submit = SubmitField("Submit")


class ThreadForm(Form):
    text = TextAreaField("Body", validators=[
        Required(message="You must enter text.")
    ])

    if not app.config["DEBUG"]:
        recaptcha = RecaptchaField()

    submit = SubmitField("Submit")
