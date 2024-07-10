"""Models for flask-feedback."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Allows to connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User profile"""

    __tablename__ = "users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50),nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    feedback = db.relationship("Feedback", backref="users", cascade="all, delete-orphan")


    @classmethod
    def register(cls, username, password, email, first_name, last_name, is_admin=False):
        """Registers a user while hashing their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        
        
        return cls( username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name, is_admin=is_admin)

        # db.session.add(user)
        # return user
    

    @classmethod
    def authenticate(cls, username, password):
        """Validates that user and password are correct
           else return false"""
        
        authentic_user = User.query.filter_by(username=username).first()

        if authentic_user and bcrypt.check_password_hash(authentic_user.password, password):
            return authentic_user
        else:
            return False
        


class Feedback(db.Model):
    """Table for Feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

    @classmethod
    def submit(cls, title, content, username):
        """Submits new feedback for username"""

        return cls(title=title, content=content, username=username)