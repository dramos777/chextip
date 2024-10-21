from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.String(200), default='')

    def set_password(self, password):
        """Define a senha do usuário após gerar seu hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'{self.username} (Admin: {self.is_admin})'

class Condominium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rb_host_ip = db.Column(db.String(45), nullable=False)
    branches = db.relationship('Branch', backref='condominium', lazy=True)

    def __str__(self):
        return self.name

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    branch_number = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    def __repr__(self):
        return f'<Branch {self.branch_number} - {self.location}>'

    def __str__(self):
        return f'Branch {self.branch_number} in {self.location}'

