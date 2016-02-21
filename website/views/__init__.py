from .home import home
from .problems import problems
from .statistics import statistics
from .account import account
from .news import news
from .register import register
from .login import login
from .errors import errors
from .admin import admin

blueprints = [
    home,
    problems,
    statistics,
    account,
    news,
    register,
    login,
    errors,
    admin
]
