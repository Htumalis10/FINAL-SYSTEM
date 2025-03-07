from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def is_administrator(self):
        return self.is_admin

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'is_admin': self.is_admin
        }
