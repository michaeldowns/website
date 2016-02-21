from flask import Blueprint, render_template, abort, flash, redirect, url_for, send_from_directory
from flask.ext.login import current_user, login_required

from ..import db
from ..models import Problem, solved_problems, ThreadPost, User
from ..forms import ProblemForm, ThreadForm

problems = Blueprint('problems', __name__)

@problems.route('/problems')
def page():
    problems = Problem.query.order_by(
        Problem.id
    ).all()

    return render_template('problems/problems.html', problems=problems)

@problems.route('/problems/<int:problem_id>', methods=["GET", "POST"])
def problem(problem_id):
    problem = Problem.query.get(problem_id)

    # This is kind of ugly but there are several different types of users that can
    # view a problem: a user that's not logged in, a user that's logged in but has not
    # solved the problem, and a user that's logged in and has solved the problem.
    # It's also possible that the problem doesn't exist
    if problem is not None:
        if current_user.is_authenticated:
            if problem not in current_user.problems:
                form = ProblemForm()

                if form.validate_on_submit():
                    if problem.solution == form.answer.data:
                        current_user.problems.append(problem)

                        db.session.commit()

                        flash("Correct!", "success")
                    else:
                        flash("Incorrect!", "danger")

                    return redirect(url_for('problems.problem',
                                            problem_id=problem_id))

                return render_template('problems/problem.html', form=form,
                                       problem=problem)
            else:
                date = db.session.query(
                    solved_problems.c.date
                ).filter(
                    solved_problems.c.user_id == current_user.id,
                    solved_problems.c.problem_id == problem.id
                ).one()

                date = date.date

                return render_template('problems/problem.html', problem=problem,
                                       date=date)
        else:
            return render_template('problems/problem.html', problem=problem)
    else:
        abort(404)

@problems.route('/thread/<int:problem_id>')
@login_required
def thread(problem_id):
    problem = Problem.query.get(problem_id)

    if problem not in current_user.problems:
        flash("You do not have access to that thread!", "danger")
        return redirect(url_for("problems.page"))

    posts = db.session.query(
        ThreadPost.text,
        ThreadPost.posted,
        ThreadPost.id,
        ThreadPost.user_id,
        ThreadPost.problem_id,
        User.username
    ).join(
        User
    ).order_by(
        ThreadPost.posted
    ).filter(
        ThreadPost.problem_id == problem_id
    ).all()

    return render_template('problems/thread.html', problem=problem, posts=posts)

@problems.route('/new_post/<int:problem_id>', methods=["GET", "POST"])
@login_required
def new_post(problem_id):
    problem = Problem.query.get(problem_id)

    if problem not in current_user.problems:
        flash("You do not have access to that thread!", "danger")
        return redirect(url_for("problems.page"))

    form = ThreadForm()

    if form.validate_on_submit():
        post = ThreadPost(
            text=form.text.data,
            user_id=current_user.id,
            problem_id=problem_id
        )

        db.session.add(post)
        db.session.commit()

        flash("Posted reply!", "success")
        
        return redirect(url_for(".thread", problem_id=problem_id))

    return render_template('problems/new_post.html', problem=problem, form=form)

@problems.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = ThreadPost.query.get(post_id)

    if post.user == current_user or current_user.moderator or current_user.admin and post is not None:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted post id {}".format(post_id), "success")
    else:
        abort(404)

    return redirect(url_for(".thread", problem_id=post.problem_id))

@problems.route('/edit_post/<int:post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = ThreadPost.query.get(post_id)

    if post.user == current_user or current_user.moderator or current_user.admin and post is not None:
        form = ThreadForm()

        if form.validate_on_submit():
            post.text = form.text.data

            db.session.commit()

            flash("Edited post id {}".format(post_id), "success")
            return redirect(url_for(".thread", problem_id=post.problem_id))

        form.text.data = post.text

        return render_template("problems/edit_post.html", form=form)

    else:
        abort(404)


        
