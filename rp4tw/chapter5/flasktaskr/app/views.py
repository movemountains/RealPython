# Views controller

from app import app, db
from flask import Flask, flash, redirect, render_template, request, \
    session, url_for, g
from functools import wraps
from app.forms import AddTask, RegisterForm, LoginForm
from app.models import FTasks, User


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash("You are logged out. Bye. :(")
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != app.config['USERNAME'] or
                request.form['password'] != app.config['PASSWORD']):
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    return render_template('login.html', error=error)


# View tasks
@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(FTasks).filter_by(status='1').order_by(
        FTasks.due_date.asc())
    closed_tasks = db.session.query(FTasks).filter_by(status='0').order_by(
        FTasks.due_date.asc())
    return render_template('tasks.html', form=AddTask(request.form),
                           open_tasks=open_tasks, closed_tasks=closed_tasks)


# Add new task
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddTask(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_task = FTasks(
            form.name.data,
            form.due_date.data,
            form.priority.data,
            '1'
        )
        db.session.add(new_task)
        db.session.commit()
        flash('New entry was successfully posted. Thanks!')
    return redirect(url_for('tasks'))


# Mark task as complete
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).update({"status": "0"})
    db.session.commit()
    flash('The task was marked as completed.')
    return redirect(url_for('tasks'))


# Delete task
@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(FTasks).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))


# Registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(
            form.name.data,
            form.email.data,
            form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, error=error)
