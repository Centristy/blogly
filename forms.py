from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('Image URL')


class UserEditForm(FlaskForm):
    """Form for editting users."""

    first_name = StringField('Username')
    last_name = StringField('Password')
    image_url = StringField('Image URL')