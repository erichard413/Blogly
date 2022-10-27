"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    with app.app_context():
        db.app = app
        db.init_app(app)

class User(db.Model):
    """User model"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(15),
                    nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    image_url = db.Column(db.String, default="/static/images/defaultpic.png")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """gets full name"""
        u = self
        return f"{u.first_name} {u.last_name}" 

