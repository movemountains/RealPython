from flask import Flask, render_template, request, session, \
    flash, redirect, url_for, g
import sqlite3
from functools import wraps

# Configuration
DATABASE = 'fblog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'VSng16ohBH3MjdOe0ftdCmit83bzR9IgoqVh7oGz7BC9suJfdEyfOQ90wEaRgcrS'

app = Flask(__name__)

# Pulls in configuration by looking for UPPERCASE vars
app.config.from_object(__name__)


# Functions used for connection to the database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != app.config['USERNAME'] or
                request.form['password'] != app.config['PASSWORD']):
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('login'))
    return wrap


@app.route("/main")
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts ORDER BY entry_date DESC')
    posts = [dict(date=row[0],
                  title=row[1],
                  post=row[2]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)


@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All field are required! Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO posts(entry_date, title, post) \
                      VALUES(date(),?,?)',
                     [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash("New entry was successfully posted.")
        return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)