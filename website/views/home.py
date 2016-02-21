from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/home')
def page():
    return render_template('home.html')
