
from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserAddForm, UserEditForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "ABC123"

connect_db(app)


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage and all users:"""


    form = UserAddForm()
    users = User.query.all()

    if form.validate_on_submit():
        User.signup(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            image_url = form.image_url.data or User.img_url.default.arg,
            )

        db.session.commit()

        flash("User Successfully Added", 'success')

        return redirect("/")
    else:
    
        return render_template('base.html', form=form, users=users)
    



@app.route('/user/edit/<int:user_id>', methods=["GET", "POST"])
def edit_profile(user_id):
    """Update profile for current user."""


    form = UserEditForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.image_url = form.image_url.data or User.image_url.default.arg,

            db.session.commit()
            flash("User Succesfully Updated", 'success')
            return redirect(f"/")

    return render_template('edit.html', form=form)


# Deletes Users    

@app.route('/user/delete/<int:user_id>', methods=["GET"])
def delete_user(user_id):
    

    User.query.filter(User.id == user_id).delete()

    db.session.commit()

    flash("User Succesfully Deleted", 'danger')
        
    return redirect('/')


