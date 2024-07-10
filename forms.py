"""Forms for flask-feedback."""


from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Optional
from flask_wtf import FlaskForm



class LoginForm(FlaskForm):
    """Form for logging a user in"""

    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)])



class RegisterForm(FlaskForm):
    """Form for registering a user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])



class FeedbackForm(FlaskForm):
    """Adds a feedback form"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])



class DeleteForm(FlaskForm):
    """Delete form"""