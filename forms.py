from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
import datetime

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('Image URL')

class UserEditForm(FlaskForm):
    """Form for editing users."""

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    image_url = StringField('Image URL')


class PostAddForm(FlaskForm):
    """Form for adding posts."""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    date = DateTimeField('Date', default=datetime.datetime.now(), validators=[DataRequired()])


class PostEditForm(FlaskForm):
    """Form for editing posts."""

    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])


class TagAddForm(FlaskForm):
    """Form for adding users."""
    name = StringField('Tag Name', validators=[DataRequired()])