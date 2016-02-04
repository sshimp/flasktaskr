# views.py (dynamic routing)

# imports
from flask import Flask, flash, redirect, render_template, \
	request, session, url_for, g
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User

# def connect_db():
# 	return sqlite3.connect(app.config['DATABASE_PATH'])

def open_tasks():
	return db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())

def closed_tasks():
	return db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text, error), 'error')

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first!')
			return redirect(url_for('login'))
	return wrap

# route handlers
@app.route('/logout/')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('user_id', None)
	session.pop('role', None)
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		# if request.form['username'] != app.config['USERNAME'] \
		# 		or request.form['password'] != app.config['PASSWORD']:
		# 	error = 'Invalid credentials. Please try again!'
		# 	return render_template('login.html', error=error)
		# else:
		# 	session['logged_in'] = True
		# 	flash('Welcome!')
		# 	return redirect(url_for('tasks'))
		if form.validate_on_submit():
			user = User.query.filter_by(name=request.form['name']).first()
			if user is not None and user.password == request.form['password']:
				session['logged_in'] = True
				session['user_id'] = user.id
				session['role'] = user.role
				flash('Welcome!')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid username or password!'
		# else:
		# 	error = 'Both fields are required!'
	return render_template('login.html', form=form, error=error)

@app.route('/tasks/')
@login_required
def tasks():
	# g.db = connect_db()
	
	# cur = g.db.execute('select name, due_date, priority, task_id from tasks where status = 1')
	# open_tasks = [
	# 	dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()
	# ]

	# cur = g.db.execute('select name, due_date, priority, task_id from tasks where status = 0')
	# closed_tasks = [
	# 	dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) for row in cur.fetchall()
	# ]

	# g.db.close()

	# open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	# closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks(),
		closed_tasks=closed_tasks()
	)

@app.route('/add/', methods=['GET','POST'])
@login_required
def new_task():
	error = None
	form = AddTaskForm(request.form)
	# g.db = connect_db()
	# name = request.form['name']
	# due_date = request.form['due_date']
	# priority = request.form['priority']
	# if not name or not due_date or not priority:
	# 	flash("All fields are required. Please try again!")
	# 	return redirect(url_for('tasks'))
	# else:
	# 	g.db.execute("""insert into tasks (name, due_date, priority, status) values (?,?,?,1)""",
	# 		[request.form['name'],request.form['due_date'],request.form['priority']])
	# 	g.db.commit()
	# 	g.db.close()
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(form.name.data, form.due_date.data, form.priority.data,'1',
				session['user_id'],datetime.utcnow())
			db.session.add(new_task)
			db.session.commit()
			flash("New entry was successfully posted. Thanks!")
		else:
			# flash('All fields are required!')
			return render_template('tasks.html', form=form, error=error)
	return render_template('tasks.html', form=form, error=error,
		open_tasks=open_tasks(), closed_tasks=closed_tasks())

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	# g.db = connect_db()
	# g.db.execute("""update tasks set status = 0 where task_id="""+str(task_id))
	# g.db.commit()
	# g.db.close()
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.update({"status":"0"})
		db.session.commit()
		flash('The task was marked as complete. Nice!')
		return redirect(url_for('tasks'))
	else:
		flash('You can only update tasks that belong to you!')
		return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	# g.db = connect_db()
	# g.db.execute("""delete from tasks where task_id="""+str(task_id))
	# g.db.commit()
	# g.db.close()
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id or session['role'] == 'admin':
		task.delete()
		db.session.commit()
		flash('The task was deleted. Why not add another one?')
		return redirect(url_for('tasks'))
	else:
		flash('You can only delete tasks that belong to you!')
		return redirect(url_for('tasks'))

@app.route('/register/', methods=['GET','POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(form.name.data, form.email.data, form.password.data,)
			try:
				db.session.add(new_user)
				db.session.commit()
				flash('Thank you for registering! Please login.')
				return redirect(url_for('login'))
			except IntegrityError:
				error = 'That username and/or email already exist.'
				render_template('register.html', form=form, error=error)
	return	render_template('register.html', form=form, error=error)


