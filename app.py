"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """redirects to List of Users"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Shows list of users"""
    users = User.query.order_by(User.id).all()

    return render_template('users.html', users = users)

@app.route('/users/new')
def new_user_form():
    """Shows form for new user"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods = ["POST"])
def add_new_user():
    """Adds the user to the list, shows the list"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)
    return render_template("user_details.html", user = user, posts = posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows form to edit a user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user = user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    """Edits a user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    
    user = User.query.get_or_404(user_id)
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Deletes a user"""
    user = User.query.filter_by(id = user_id)
    user.delete()
    user.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Shows form to add a post"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('add_post_form.html', user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def add_post(user_id):
    """Adds the post"""
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(user_id = user_id, title = title, content = content)
    db.session.add(new_post)
    db.session.commit()
    new_post_id = int(new_post.id)

    tag_ids = request.form.getlist("tags")
    for tag in tag_ids:
        t = Tag.query.get(int(tag))
        post_tag = PostTag(post_id = new_post_id, tag_id = t.id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f'/users/{new_post.user_id}/posts/{new_post.id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(user_id, post_id):
    """Shows post to user"""
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    tags = Post.query.get(post_id).tags
    return render_template('post_details.html', user = user, post = post, tags = tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete')
def delete_post(user_id, post_id):
    """Deletes a post"""
    p = Post.query.filter_by(id = post_id)
    p.delete()
    p.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def edit_post_form(user_id, post_id):
    """Shows form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post_form.html", post = post, user_id = user_id, tags = tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods = ["POST"])
def edit_post(user_id, post_id):
    """Edits a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.created_at = datetime.datetime.now()

    db.session.add(post)
    db.session.commit()
    post_id = post.id

    post = Post.query.get(post_id)
    tags = post.tags
    for tag in tags:
        d = PostTag.query.filter_by(post_id = post_id)
        d.delete()
        db.session.commit()
        

    tag_ids = request.form.getlist("tags")
    for tag in tag_ids:
        t = Tag.query.get(int(tag))
        post_tag = PostTag(post_id = post_id, tag_id = t.id)
        db.session.add(post_tag)
        db.session.commit()
    
    post = User.query.get_or_404(user_id)
    return redirect(f'/users/{user_id}/posts/{post_id}')

@app.route('/tags')
def show_tags():
    """Shows list of tags"""
    tags = Tag.query.order_by(Tag.id).all()

    return render_template('tags.html', tags = tags)
    

@app.route('/tags/<int:tag_id>')
def show_posts_for_tag(tag_id):
    """Shows list of posts for the tag"""
    tag = Tag.query.get(tag_id)
    posts = Tag.query.get(tag_id).posts

    return render_template('posts_for_tag.html', tag = tag, posts =posts)

@app.route('/tags/new')
def add_tag_form():
    """Shows form to add a tag"""
    return render_template("new_tag_form.html")

@app.route('/tags/new', methods = ["POST"])
def add_tag():
    """Adds the tag"""
    name = request.form["name"]

    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Deletes a tag"""
    t = Tag.query.filter_by(id = tag_id)
    t.delete()
    t.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Shows form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag_form.html", tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods = ["POST"])
def edit_tag(tag_id):
    """Edits a tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()
    
    tag = Tag.query.get_or_404(tag_id)
    return redirect(f'/tags/{tag_id}')