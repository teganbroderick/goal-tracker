# Goal Tracker

Goal tracker lets you sign up/log in, add goals to a list, and then edit them.

Tech Stack: Python, HTML, CSS, Flask, Jinja, PostgreSQL, SQLAlchemy

## <a name="installation"></a>Installation

### Prerequisites

You must have the following installed to run the app:

- PostgreSQL
- Python 3.x

### Run App on your local computer

Clone or fork repository:
```
$ git clone https://github.com/teganbroderick/goal-tracker
```
Create and activate a virtual environment inside your goal tracker directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database 'goals':
```
$ createdb goals
```
Run model.py interactively in the terminal, and create database tables:
```
$ python3 -i model.py
>>> db.create_all()
>>> quit()
```
Run the app from the command line.
```
$ python server.py
```