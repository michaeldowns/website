"""
db.py
-----
Handles database migrations. Requires that a database has been set up.

Usage when initializing database for the first time:
-Delete alembic_version table from database
-Delete migrations folder
-Enter the following commands into the shell:
 python db.py db init
 python db.py db migrate
 python db.py db upgrade

Init creates the migrations folder 
Migrate checks for changes in the Flask app's ORM schema
Upgrade pushes changes to the database paired with our app

Usage when updating/migrating pre-existing database
-Enter the following commands into the shell:
 python db.py db migrate
 python db.py db upgrade
"""
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from website import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
