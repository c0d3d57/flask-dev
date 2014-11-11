#from fla import app
from flask.ext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:ignition9091@localhost:5432/mydb'
db = SQLAlchemy(app)