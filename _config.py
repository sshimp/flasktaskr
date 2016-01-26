import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
# USERNAME = 'admin'
# PASSWORD = 'admin'
WTF_CSRF_ENABLED = True 
SECRET_KEY = '\x002\x05F\x0c\xd3\xf8Z\x17\x8aXZ\xdc,6\xb3\x16\xebV\xb2\xfa\xbe\xa1\xe1'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH