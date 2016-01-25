# views.py (dynamic routing)

#import sqlite3  # replaced by SQLAlchemy
from functools import wraps
from flask import Flask, flash, redirect, render_template, \
	request, session, url_for, g
from forms import AddTaskForm
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task

# def connect_db():
# 	return sqlite3.connect(app.config['DATABASE_PATH'])

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
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] \
				or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials. Please try again!'
			return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			flash('Welcome!')
			return redirect(url_for('tasks'))
	return render_template('login.html')

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

	open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

	return render_template(
		'tasks.html',
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
	)

@app.route('/add/', methods=['GET','POST'])
@login_required
def new_task():
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
			new_task = Task(form.name.data, form.due_date.data, form.priority.data,'1')
			db.session.add(new_task)
			db.session.commit()
			flash("New entry was successfully posted. Thanks!")
	
	return redirect(url_for('tasks'))

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	# g.db = connect_db()
	# g.db.execute("""update tasks set status = 0 where task_id="""+str(task_id))
	# g.db.commit()
	# g.db.close()
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
	db.session.commit()
	flash('The task was marked as complete. Nice!')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	# g.db = connect_db()
	# g.db.execute("""delete from tasks where task_id="""+str(task_id))
	# g.db.commit()
	# g.db.close()
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).delete()
	db.session.commit()
	flash('The task was deleted! Why not add a new one?')
	return redirect(url_for('tasks'))



