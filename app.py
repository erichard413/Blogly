"""Blogly application."""



from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag, get_posts_by_id, get_post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']="pugsarecool24"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home_page():
    """Home"""
    posts = Post.query.all()
    tags = Tag.query.all()
    return render_template("/home.html", posts=posts, tags=tags)

@app.route("/users")
def list_users():
    """list of users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/<int:user_id>")
def user_information(user_id):
    """detail of user"""
    user = User.query.get_or_404(user_id)
    post = get_posts_by_id(user_id)
    return render_template("user.html", user=user, post=post)

@app.route("/users/new")
def add_user():
    """add user page"""
    return render_template("adduser.html")

@app.route("/users/new", methods=["POST"])
def create_new_user():
    """creates a new user"""
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = None
    if request.form["img_url"]:
        img = request.form["img_url"]
        
    new_user = User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """delete user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:user_id>/edit")
def edit_user_page(user_id):
    """add user page"""
    user = User.query.get_or_404(user_id)
    first = user.first_name
    last = user.last_name
    img = user.image_url
    return render_template('edituser.html', user=user, first = first, last=last,img=img)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """add user page"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    img = None
    if request.form["img_url"]:
        user.image_url = request.form["img_url"]
        
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """add post form"""
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template("addpost.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """add post form"""
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for tag in tags:
        pt = PostTag(post_id=new_post.id, tag_id=tag.id)
        db.session.add(pt)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_posts(post_id):
    post = Post.query.get(post_id)
    user_id = post.user_id
    user = User.query.get(user_id)
    return render_template("post.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    return render_template("editpost.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """add post form"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete post from id"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route("/tags")
def show_tags_page():
    """this directs user to tags list"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route("/tags/new")
def add_tags_page():
    """render page to create new tag"""
    posts = Post.query.all()
    return render_template('addtag.html', posts = posts)

@app.route("/tags/new", methods=['POST'])
def create_new_tag():
    """create new tag"""
    tag_name = request.form["tag"]
    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()
    tag = Tag.query.filter_by(name=tag_name).first()
    posts = [post_id for post_id in request.form.getlist("tag_post")]
    for post_id in posts:
        post = Post.query.get(post_id)
        post.tags.append(tag)
    db.session.commit() 
    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def show_posts_by_tag(tag_id):
    """renders page with tagged posts"""
    tag = Tag.query.get(tag_id)

    return render_template("tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_tags_load(tag_id):
    """renders edit tag page"""
    tag = Tag.query.get(tag_id)
    posts = Post.query.all()
    return render_template("edittag.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tags(tag_id):
    """edits tag name"""
    tag_name = request.form["tag"]
    tag = Tag.query.get(tag_id)
    tag.name = tag_name
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """delete tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")


