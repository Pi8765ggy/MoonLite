import sqlite3
import click
from flask import current_app, g

# Returns the database, connected to the sqlite3 file.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        # Enables foreign keys for SQLite
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db

# Closes the database
def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initializes the database. Should NOT be run if you want to save the data inside.
def init_db():
    db = get_db()
    
    # Open the schema file and execute the SQL instructions
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# initializes the database to the app produced by the factory
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# Creates flask command for initializing database.
@click.command('init-db')
def init_db_command():
    # Clears all existing data. Creates new tables.
    init_db()
    click.echo('Initialized database.')
