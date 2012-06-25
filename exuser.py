from flask import Flask, render_template
from flask import Response, redirect, flash
from flask.ext.lastuser import LastUser
from flask.ext.lastuser.sqlalchemy import UserManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.lastuser.sqlalchemy import UserBase

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.py')
lastuser = LastUser(app)
db = SQLAlchemy(app)

class User(db.Model, UserBase):
    __tablename__ = 'user'

lastuser.init_usermanager(UserManager(db, User))


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login')
@lastuser.login_handler
def login():
    return {'scope': 'id'}

@app.route('/logout')
@lastuser.logout_handler
def logout():
    flash(u"You are now logged out", category='info')
    return get_next_url()


@app.route('/login/redirect')
@lastuser.auth_handler
def lastuserauth():
    # Save the user object
    db.session.commit()
    return redirect(get_next_url())

@app.route('/new', methods=['GET', 'POST'])
@lastuser.requires_login
def newspace():
    return render_template('new.html')


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'), code=301)


@lastuser.auth_error_handler
def lastuser_error(error, error_description=None, error_uri=None):
    if error == 'access_denied':
        flash("You denied the request to login", category='error')
        return redirect(get_next_url())
    return Response(u"Error: %s\n"
                    u"Description: %s\n"
                    u"URI: %s" % (error, error_description, error_uri),
                    mimetype="text/plain")
