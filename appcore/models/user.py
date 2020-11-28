from werkzeug.security import generate_password_hash, check_password_hash
from appcore.models import db
from datetime import datetime
from sqlalchemy.orm import validates
import re


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(11), nullable=True)
    name = db.Column(db.String(32), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_deleted = db.Column(db.Boolean, server_default="0", nullable=False)

    @property
    def password(self):
        raise NotImplementedError('Cannot read password of user!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise 
        if not re.match("[^@]+@[^@]+\.[^@]+", email):  # noqa: F401, F403
            raise 

        return email

