from flask import Flask, request, flash, url_for, redirect, render_template
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.sqlite3'
app.config['SECRET_KEY'] = "asdjkbakjsbdjkbakds"

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return 'User(' + self.username + ', ' + self.email +')'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), unique=True, nullable=False)
	date_posted = db.Column(db.DateTime , nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, unique=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return 'Post(' + self.title + ', ' + self.date_posted.strftime('%B %d %Y - %H:%M:%S') + ')'

posts = [
	{'author' : 'auth',
	'title': 'title',
	'content': 'Lorem Ipsum Lorem Ipsum',
	'date_posted': ''}
]