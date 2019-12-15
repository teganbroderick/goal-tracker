from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Task, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Verify whether session exists, render index page"""
    if 'user_id' in session: #if session exists
        user = User.query.filter_by(user_id=session['user_id']).first()
        tasks = Task.query.filter_by(user_id=session['user_id']).all()
        return render_template("tasks.html", user=user, tasks=tasks)
    else:
        return render_template("index.html")


@app.route('/signup_process', methods=["POST"])
def signup_process():
    """Check to see if user exists, if not, add user to user table"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first() #get user via entered email address

    if user == None: #if user is not in the users table
        #add user to database
        user_info = User(fname=fname, lname=lname, email=email, password=password)
        db.session.add(user_info)
        db.session.commit()

        user = User.query.filter_by(email=email).first() #get user object
        session['user_id'] = user.user_id #add user to session 
        tasks = Task.query.filter_by(user_id=session['user_id']).all() #get tasks
        flash("Logged in!")
        return render_template("tasks.html", user=user, tasks=tasks)
    else: 
        flash("A user with that email address already exists.")
        return redirect("/")


@app.route('/logout')
def logout():
    """delete user_id info from session and log user out"""
    
    del session["user_id"]
    flash("Logged out!")
    return redirect('/')


@app.route('/login_process', methods=["POST"])
def login_process():
    """Verify email and password credentials, log user in if they are correct"""

    email = request.form.get("email")
    password = request.form.get("password")

    #check to see if email address and password match a user in the users table
    user = User.query.filter_by(email=email, password=password).first()

    if user == None:
        flash("Wrong email or password. Try again!")
        return redirect('/')
    else:
        #add user to session
        session['user_id'] = user.user_id
        tasks = Task.query.filter_by(user_id=session['user_id']).all()
        flash("Logged in!")
        return render_template("tasks.html", user=user, tasks=tasks)


@app.route('/add_task', methods=["POST"])
def add_task():
    """add task to list of tasks"""

    task_name = request.form.get("task_name")

    task_to_verify = Task.query.filter_by(user_id=session['user_id'], 
                    task_name=task_name).first()
    
    if task_to_verify == None: #if task not in db
        new_task = Task(user_id=session['user_id'], 
                    task_name=task_name)
        db.session.add(new_task)
        db.session.commit()
    else:
        flash("Goal already in your list")
    
    user = User.query.filter_by(user_id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('tasks.html', tasks=tasks, user=user)


@app.route('/edit_task', methods=["POST"])
def edit_task():
    """edit task in list of tasks"""

    task_name = request.form.get("task_name")
    print(task_name)
    new_task_name = request.form.get("new_task_name")
    print(new_task_name)

    #find task in db
    task_to_change = Task.query.filter(Task.task_name == task_name).first()
    print(task_to_change)
    task_to_change.task_name = new_task_name

    db.session.commit()

    user = User.query.filter_by(user_id=session['user_id']).first()
    tasks = Task.query.filter_by(user_id = session['user_id'])
    return render_template('tasks.html', tasks=tasks, user=user)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')