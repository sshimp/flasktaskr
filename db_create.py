# project/db_create.py

# import sqlite3
# from _config import DATABASE_PATH

from views import db
from models import Task
from datetime import date

# with sqlite3.connect(DATABASE_PATH) as connection:

# 	c = connection.cursor()

# 	c.execute("""
# 		create table tasks(
# 			task_id INTEGER PRIMARY KEY AUTOINCREMENT,
# 			name TEXT NOT NULL,
# 			due_date TEXT NOT NULL,
# 			priority INTEGER NOT NULL,
# 			status INTEGER NOT NULL
# 			)""")

# 	c.execute("""insert into tasks (name, due_date, priority, status)
# 				values ('Finish this tutorial!','03/25/2015',10,1)""")

# 	c.execute("""insert into tasks (name, due_date, priority, status)
# 				values ('Finish Real Python Course Part II','03/25/2015',10,1)""")

db.create_all()

db.session.add(Task("Finish this tutorial",date(2015,3,13),10,1))
db.session.add(Task("Finish Real Python",date(2015,3,13),10,1))

db.session.commit()