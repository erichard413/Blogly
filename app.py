"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return redirect("/users")

@app.route("/users")
def list_users():
    """list of users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/<int:user_id>")
def user_information(user_id):
    """detail of user"""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

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


