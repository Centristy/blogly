
from flask import Flask, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from forms import UserAddForm, UserEditForm, PostAddForm, PostEditForm, TagAddForm
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
    posts = (Post.query.filter(Post.user_id == user_id).order_by(Post.id.desc()).all())
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
            return redirect(f"/users/{user_id}")

    return render_template('edit_users.html', form=form, user=user)


# Deletes Users    

@app.route('/users/<int:user_id>/delete', methods=["GET"])
def delete_user(user_id):
    
    Post.query.filter(Post.user_id == user_id).delete()
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    flash("User Succesfully Deleted", 'danger')
        
    return redirect('/')



################################## POST ROUTES ####################################






@app.route('/posts', methods=["GET", "POST"])
def all_posts():

    

    posts = (Post.query.order_by(Post.id.desc()).all())
    

    return render_template('all_posts.html', posts=posts)


@app.route('/posts/<int:post_id>', methods=["GET", "POST"])
def one_post(post_id):

    

    posts = (Post.query.filter(Post.id == post_id).order_by(Post.id.desc()).all())
    

    return render_template('all_posts.html', posts=posts)


@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def add_post(user_id):
    

    form = PostAddForm()
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    

    if form.validate_on_submit():

        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        post = Post(
            title = form.title.data,
            content = form.content.data,
            date = form.date.data,
            user_id = user_id,
            tags = tags

        )


        db.session.add(post)
        db.session.commit()

        flash("Post Succesfully Created", 'success')
        
        return redirect(f'/users/{user_id}')
    
    else:

        return render_template('add_post.html', form=form, user=user, tags=tags)
    

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    form = PostEditForm(obj=post)
    tags = Tag.query.all()

    

    if form.validate_on_submit():

        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        post.title = form.title.data,
        post.content = form.content.data,
        post.tags = tags

        db.session.commit()

        flash("Post Succesfully Edited", 'success')
        
        return redirect(f'/users/{user_id}')
    
    else:

        return render_template('edit_post.html', form=form, user=user, tags=tags)
    

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=["GET", "POST"])
def delete_post(user_id, post_id):


    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    
    return redirect(f'/users/{user_id}')





############################## TAG ROUTES ###############################


@app.route('/tags', methods=["GET", "POST"])
def all_tags():

    form = TagAddForm()
    tags = Tag.query.all()


    if form.validate_on_submit():

        tag = Tag(
            name = form.name.data

        )

        db.session.add(tag)
        db.session.commit()

        flash("Tag Succesfully Created", 'success')
        
        return redirect(f'/tags')
    
    else:

        return render_template('all_tags.html', form=form, tags=tags)
    

@app.route('/tags/<int:tag_id>/edit', methods=["GET", "POST"])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    form = TagAddForm()

    if form.validate_on_submit():

        tag.name = form.name.data

        db.session.commit()

        flash("Tag Succesfully Edited", 'success')
        
        return redirect(f'/tags')
    
    else:

        return render_template('edit_tag.html', form=form)


@app.route('/tags/<int:tag_id>/delete', methods=["GET"])
def delete_tag(tag_id):


    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    
    return redirect('/tags')

