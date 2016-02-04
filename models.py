# models.py

from views import db
from datetime import datetime

class Task(db.Model):
	__tablename__ = "tasks"

	task_id = db.Column(db.Integer, primary_key=True) # will autoincrement by default
	name = db.Column(db.String, nullable=False)
	due_date = db.Column(db.Date, nullable=False)
	priority = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	posted_date = db.Column(db.Date, default=datetime.utcnow())

	def __init__(self, name, due_date, priority, status, user_id, posted_date):
		self.name = name
		self.due_date = due_date
		self.priority = priority
		self.status = status
		self.user_id = user_id
		self.posted_date = posted_date

	def __repr__(self):
		return '<name {0}>'.format(self.name)

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	tasks=db.relationship('Task',backref='poster')
	role=db.Column(db.String, default='user')

	def __init__(self, name=None, email=None, password=None, role=None):
		self.name = name
		self.email = email
		self.password = password
		self.role = role

	def __repr__(self):
		return '<User {0}>'.format(self.name)