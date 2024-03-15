from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms.validators import DataRequired
import datetime

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('Image URL')

class UserEditForm(FlaskForm):
    """Form for editing users."""

    first_name = StringField('Username')
    last_name = StringField('Password')
    image_url = StringField('Image URL')


class PostAddForm(FlaskForm):
    """Form for adding posts."""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    date = DateField('Date', default=datetime.date.today())


class PostEditForm(FlaskForm):
    """Form for editing posts."""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])