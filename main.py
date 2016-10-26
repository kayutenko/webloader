from __future__ import print_function
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from forms import WelcomeScreenForm, CreateObjectForm
import os
import sqlite3
import sys
import json
from parse_webpage import parse_doc



app = Flask(__name__)
app.config.from_object(__name__)
from time import sleep

from celery import Celery
import sys

DEFAULT_PORT = 5000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)



app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'webloader.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    CELERY_BACKEND= 'mongodb://localhost/celery',
    CELERY_BROKER_URL= 'amqp://guest:guest@localhost:5672//'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def make_celery(app):
    celery = Celery('main', backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

log = open('log.txt', 'w', encoding='utf-8')

# session['logged_in'] = False

@app.route('/', methods=['GET', 'POST'])
def hello_loader():
    if session['logged_in']:
        db = get_db()
        data = db.execute("select email, site_to_parse from users order by id desc").fetchone()
        site_to_parse = data['site_to_parse']
        eprint(site_to_parse)
        parse_doc(site_to_parse, os.path.join('.\\templates\\parsed_site.html'))
        return render_template("index.html", current_user=data['email'])
    else:
        return redirect(url_for("welcome_screen"))

@app.route('/welcome_screen', methods=['GET', 'POST'])
def welcome_screen():
    form = WelcomeScreenForm(request.form)
    db = get_db()
    if request.method == 'POST' and form.validate():
        db.execute("insert into users (site_to_parse, email, password) values ( ?, ?,  ? ) ", [form.site_to_parse.data, form.email.data, form.password.data])
        db.commit()
        session['logged_in'] = True
        return redirect("/")
    return render_template("welcome_screen.html", form=form)

@app.route('/get_parsing_config', methods=['POST'])
def get_parsing_config():
    request.get_json()
    if request.method == 'POST':
        objects = request.get_json(cache=True, force=True)
        task_id = celery_parse_site.delay()
        return jsonify({'status': 'OK', 'task_id': str(task_id)})
    return jsonify({'status': 'OK'})

@celery.task
def celery_parse_site():
    return 'JR'

@app.route('/results/<task_id>')
def get_parsed_data(task_id):
    async_result = celery.AsyncResult(task_id)
    return jsonify({
        'ready': async_result.ready(),
        'status': async_result.status,
        'result': str(async_result.result),
        'task_id': str(async_result.task_id)
    })

if __name__ == '__main__':
    app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)