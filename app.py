
from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from forms import UserAddForm, UserEditForm, PostAddForm, PostEditForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "ABC123"

connect_db(app)



########################### USER ROUTES ##########################


@app.route('/', methods=["GET", "POST"])
def homepage():
    """Show homepage and all users:"""


    form = UserAddForm()
    users = User.query.all()

    if form.validate_on_submit():
        User.signup(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            image_url = form.image_url.data or User.img_url.default.arg
            )

        db.session.commit()

        flash("User Successfully Added", 'success')

        return redirect("/")
    else:
    
        return render_template('homepage.html', form=form, users=users)
    


    
@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def view_profile(user_id):
    """GET profile for specific user + Posts """


    user = User.query.get_or_404(user_id)
    posts = (Post.query.filter(Post.user_id == user_id).order_by(Post.date.desc()).all())
    form = UserAddForm()

    return render_template('details.html', user=user, form=form, posts=posts)

    

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
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

@app.route('/users/<int:user_id>/delete', methods=["GET"])
def delete_user(user_id):
    
    Post.query.filter(Post.user_id == user_id).delete()
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    flash("User Succesfully Deleted", 'danger')
        
    return redirect('/')



################################## POST ROUTES ####################################



# **GET */users/[user-id]/posts/new :*** Show form to add a post for that user.

# **POST */users/[user-id]/posts/new :*** Handle add form; add post and redirect to the user detail page.


@app.route('/posts', methods=["GET", "POST"])
def all_posts():

    

    posts = (Post.query.order_by(Post.date.desc()).all())
    form = UserAddForm()

    return render_template('all_posts.html', posts=posts, form=form)




@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    

    form = PostAddForm()
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():

        post = Post(
            title = form.title.data,
            content = form.content.data,
            user_id = user_id

        )

        db.session.add(post)
        db.session.commit()

        flash("Post Succesfully Created", 'success')
        
        return redirect(f'/users/{user_id}')
    
    else:

        return render_template('add_post.html', form=form, user=user)
    

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    form = PostEditForm(obj=post)

    if form.validate_on_submit():

        post.title = form.title.data,
        post.content = form.content.data,

        db.session.commit()

        flash("Post Succesfully Edited", 'success')
        
        return redirect(f'/users/{user_id}')
    
    else:

        return render_template('edit_post.html', form=form, user=user)
    

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=["GET", "POST"])
def delete_post(user_id, post_id):


    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    
    return redirect(f'/users/{user_id}')






# **GET */posts/[post-id] :*** Show a post. Show buttons to edit and delete the post.

# **GET */posts/[post-id]/edit :*** Show form to edit a post, and to cancel (back to user page).

# **POST */posts/[post-id]/edit :*** Handle editing of a post. Redirect back to the post view.

# **POST */posts/[post-id]/delete :*** Delete the post.

