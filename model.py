from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        primary_key=True, 
                        autoincrement=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """Return a human-readable representation of a user"""

        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>"


class Task(db.Model):
    """Data model for a goal."""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, 
                        primary_key=True,   
                        autoincrement=True)
    task_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    task_name = db.Column(db.String(50), nullable=False)
    task_description = db.Column(db.String(100), nullable=False)
    task_active = db.Column(db.Boolean, default=True, nullable=False)


    def __repr__(self):
        """Return a human-readable representation of a goal"""

        return f"<Task task_id={self.task_id} user_id={self.user_id} task_name={self.task_name} task_description={self.task_description}>"

def connect_to_db(app, db_uri="postgresql:///todo"):
    """Connect the database to the Flask app"""

    # Configure to use the database.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")