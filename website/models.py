from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from . import app, bcrypt, db

solved_problems = db.Table('solved_problems',
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("problem_id", db.Integer, db.ForeignKey("problems.id")),
    db.Column("date", db.DateTime, default=datetime.utcnow),
    db.PrimaryKeyConstraint("user_id", "problem_id")
)


class User(db.Model, UserMixin):
    """
    To do: Massive docstring detailing each field. Describe UserMixin.
    """
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(app.config['USERNAME_LENGTH']), unique=True)
    email = db.Column(db.String(app.config['EMAIL_LENGTH']), unique=True)
    _password = db.Column(db.String(app.config['PASSWORD_LENGTH']))
    email_confirmed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('ThreadPost', backref='user')
    moderator = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    problems = db.relationship("Problem", secondary=solved_problems,
                               backref="users")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)


class Problem(db.Model):
    """
    To do: Docstring detailing the fields in this model
    """
    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True)
    text = db.Column(db.Text)
    difficulty = db.Column(db.Integer)
    solution = db.Column(db.String(128))
    posts = db.relationship('ThreadPost', backref='problem')

    def __init__(self, title, text, difficulty, solution):
        self.title = title
        self.text = text
        self.difficulty = difficulty
        self.solution = solution

    def __repr__(self):
        return "<Problem {}: {}>".format(self.id, self.title)


class NewsPost(db.Model):
    __tablename__ = "news_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    text = db.Column(db.Text)
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return "<News Post: {}".format(self.title)


class ThreadPost(db.Model):
    __tablename__ = "thread_posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text, user_id, problem_id):
        self.text = text
        self.user_id = user_id
        self.problem_id = problem_id

    
