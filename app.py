"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "SECRET!"

debug = DebugToolbarExtension(app)

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

connect_db(app)
db.create_all()



### HOME REDIRECT
@app.route('/')
def index():
    """Redirect to home page"""
    return redirect('/users')

### HOME
@app.route('/users')
def show_all_users_page():
    """Route to shows all users and links to add user and view tags"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("index.html", users=users)

######################## USER ROUTES ########################

@app.route('/users/<user_id>')
def user_details(user_id):
    """Route to view details about a user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/user_detail.html", user=user)

### CREATE VIEW
@app.route('/users/new')
def go_to_add_user_page():
    """Route to add user"""
    return render_template("users/add_user.html")

### CREATES
@app.route('/users/new', methods=["POST"])
def add_user():
    """Route that adds the user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    if request.form['image_url'] != "":
        image_url = request.form['image_url']
    else:
        image_url = DEFAULT_IMAGE_URL
    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

### UPDATE VIEW
@app.route('/users/<user_id>/edit')
def go_to_edit_user_details_page(user_id):
    """Route to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit_user.html", user=user)

### UPDATES
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_details(user_id):
    """Route that edits user info"""
    user = User.query.filter_by(id=user_id).one()

    if request.form['first_name'] != "":
        user.first_name = request.form['first_name']
    if request.form['last_name'] != "":
        user.last_name = request.form['last_name']
    if request.form['image_url'] != "":
        user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')

### DELETES
@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Route that deletes a user"""
    user = User.query.filter_by(id=user_id).one()

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')




######################## POST ROUTES ########################

@app.route('/posts/<post_id>')
def post_details(post_id):
    """Route to view a post"""
    post = Post.query.filter_by(id = post_id).one()
    return render_template("posts/post_detail.html", post=post)

### CREATE VIEW
@app.route('/users/<int:user_id>/posts/new')
def go_to_add_post_page(user_id):
    """Route to add a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/add_post.html", user=user, tags=tags)

### CREATES
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Route that adds a new post"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist('checked_tag')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, creator_id=user_id,tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

### UPDATE VIEW
@app.route('/posts/<post_id>/edit')
def go_to_edit_post_page(post_id):
    """Route to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post/edit_post.html", post=post,tags=tags)

### UPDATES
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_details(post_id):
    """Route that edits a post"""
    post = Post.query.filter_by(id=post_id).one()

    if request.form['title'] != "":
        post.title = request.form['title']
    if request.form['content'] != "":
        post.content = request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist('checked_tag')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

### DELETES
@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Route that deletes a post"""
    post = Post.query.filter_by(id=post_id).one()

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.creator_id}')



######################## TAG ROUTES ########################

@app.route('/tags')
def view_tags_page():
    """Route to view tags"""
    tags = Tag.query.all()
    return render_template("tags/view_tags.html",tags=tags)

### CREATE VIEW
@app.route('/tags/new')
def go_to_add_tags_page():
    """Route to add a tag"""
    tags = Tag.query.all()
    return render_template("tags/create_tags.html",tags=tags)

### CREATES
# Needs error handling if tag name already exists
@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Route that adds a tag"""
    if request.form['name'] != "":
        name = request.form['name']

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags/new')

### UPDATE VIEW
@app.route('/tags/<int:tag_id>/edit')
def view_tag_details(tag_id):
    """Route to edit a tag"""
    tag = Tag.query.filter_by(id=tag_id).one()
    return render_template('tags/edit_tag.html',tag=tag)

### UPDATES
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_details(tag_id):
    """Route that edits a tag"""
    tag = Tag.query.filter_by(id=tag_id).one()

    if request.form['name'] != "":
        tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

### DELETES
@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Route that deletes a tag"""
    tag = Tag.query.filter_by(id=tag_id).one()

    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')