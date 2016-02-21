from flask import Blueprint, render_template
from sqlalchemy import desc, func

from .. import db
from ..models import *

statistics = Blueprint('statistics', __name__)

@statistics.route('/statistics')
def page():
    num_users = User.query.count()

    leader = db.session.query(
        User,
        func.count(solved_problems.c.user_id).label('total')
    ).join(
        solved_problems
    ).group_by(
        User
    ).order_by(
        'total DESC'
    ).first()[0].username    

    num_problems = Problem.query.count()

    easiest_problem = db.session.query(
        Problem,
        func.count(solved_problems.c.user_id).label('total')
    ).join(
        solved_problems
    ).group_by(
        Problem
    ).order_by(
        'total DESC'
    ).first()[0].title

    hardest_problem = db.session.query(
        Problem,
        func.count(solved_problems.c.user_id).label('total')
    ).join(
        solved_problems
    ).group_by(
        Problem
    ).order_by(
        'total'
    ).first()[0].title
    
    return render_template('statistics.html',
                           num_users=num_users,
                           leader=leader,
                           num_problems=num_problems,
                           easiest_problem=easiest_problem,
                           hardest_problem=hardest_problem)
