from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


#***User*** model for SQLAlchemy. Put this in a ***models.py*** file.

# It should have the following columns:

# - ***id***, an autoincrementing integer number that is the primary key
# - ***first_name*** and ***last_name***
# - ***image_url*** for profile images

# Make good choices about whether things should be required, have defaults, and so on.


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    @classmethod
    def signup(cls, first_name, last_name, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        user = User(
            first_name = first_name,
            last_name = last_name,
            image_url=image_url
        )

        db.session.add(user)
        return user

    
    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    

class Post(db.Model):
    """Posts in the system"""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    date = db.Column(
        db.Date,
        default= datetime.datetime.today(),
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    users = db.relationship('User')




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)