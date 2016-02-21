from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required

from .. import db
from ..util.decorators import admin_required
from ..forms import NewsPostForm, EditNewsPostForm, EditUserForm, EditProblemForm
from ..models import NewsPost, User, Problem

admin = Blueprint('admin', __name__)

@admin.route("/admin/news/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_news():
    add_news_form = NewsPostForm(prefix="add_")

    if add_news_form.validate_on_submit():
        new_news_post = NewsPost(
            title=add_news_form.title.data,
            text=add_news_form.text.data
        )

        db.session.add(new_news_post)
        db.session.commit()

        flash("Added news post!", "success")
        
        return redirect(url_for(".admin_news"))

    news_posts = NewsPost.query.order_by(
        NewsPost.posted.desc(),
        NewsPost.id
    ).all()

    edit_news_forms = []
    for news_post in news_posts:
        edit_news_form = EditNewsPostForm(prefix="edit_{}_".format(news_post.id))

        if edit_news_form.validate_on_submit():
            if edit_news_form.delete.data:
                db.session.delete(news_post)

                flash("Deleted news post {}!".format(news_post.id), "success")
            else:
                news_post.title = edit_news_form.title.data
                news_post.text = edit_news_form.text.data

                flash("Edited news post {}!".format(news_post.id), "success")

            db.session.commit()
                
            return redirect(url_for(".admin_news"))

        edit_news_form.title.data = news_post.title
        edit_news_form.text.data = news_post.text

        edit_news_forms.append(edit_news_form)

    return render_template("admin/news.html", add_news_form=add_news_form,
                           edit_news_forms=edit_news_forms)
    
@admin.route("/admin/user/<username>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_user(username):
    form = EditUserForm()

    user = User.query.filter_by(
        username=username
    ).first_or_404()

    if form.validate_on_submit():
        if form.delete_user.data:
            flash("Deleted {}".format(user.username), "success")

            db.session.delete(user)
            
            db.session.commit()
            return redirect(url_for("home.page"))
        else:
            user.email = form.email.data
            user.username = form.username.data
            user.email_confirmed = form.email_confirmed.data
            user.moderator = form.moderator.data

            if form.password.data != '':
                user.password = form.password.data


            db.session.commit()

            flash("Edited {}".format(user.username), "success")
            return redirect(url_for(".admin_user", username=form.username.data))

    form.email.data = user.email
    form.username.data = user.username
    form.email_confirmed.data = user.email_confirmed
    form.moderator.data = user.moderator
    

    return render_template("admin/user.html", form=form)

@admin.route("/admin/problem/<int:problem_id>", methods=["GET", "POST"])
@login_required
@admin_required
def admin_problem(problem_id):
    form = EditProblemForm()

    problem = Problem.query.get(problem_id)

    if form.validate_on_submit():
        problem.title = form.title.data
        problem.text = form.text.data
        problem.difficulty = form.difficulty.data
        problem.solution = form.solution.data

        db.session.commit()

        flash("Successfully edited problem!", "success")

        return redirect(url_for(".admin_problem", problem_id=problem_id))

    form.title.data = problem.title
    form.text.data = problem.text
    form.difficulty.data = problem.difficulty
    form.solution.data = problem.solution

    
    return render_template("admin/problem.html", form=form)


@admin.route("/admin/add_problem", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_problem():
    form = EditProblemForm()

    if form.validate_on_submit():
        problem = Problem(
            title=form.title.data,
            text=form.text.data,
            difficulty=form.difficulty.data,
            solution=form.solution.data
        )

        db.session.add(problem)
        db.session.commit()

        flash("Added problem!", "success")

        return redirect(url_for(".admin_add_problem"))

    return render_template("admin/add_problem.html", form=form)
