from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask.ext.login import login_user, logout_user

from .. import db
from ..forms import LoginForm, EmailForm, PasswordForm
from ..models import User
from ..util.decorators import require_unauthed
from ..util.security import ts
from ..util.mail import send_email

login = Blueprint('login', __name__)

@login.route('/login', methods=["GET", "POST"])
@require_unauthed
def page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).first()

        login_user(user, form.remember_me.data)

        flash("Logged in successfully!", "success")

        # add security later
        next = request.args.get('next')

        return redirect(next or url_for('home.page'))

    return render_template('login.html', form=form)

@login.route('/logout')
def logout():
    logout_user()

    flash("Logged out successfully!", "success")

    return redirect(url_for('home.page'))

@login.route('/reset', methods=["GET", "POST"])
@require_unauthed
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user is not None and user.email_confirmed:
            subject = "Password reset requested"

            # Here we use the URLSafeTimedSerializer we created in `util` at the
            # beginning of the chapter
            token = ts.dumps(user.email, salt='recover-key')

            recover_url = url_for('login.reset_with_token', token=token,
                                  _external=True)

            html = render_template('email/recover.html',
                                   recover_url=recover_url)

            send_email(user.email, subject, html)

        flash("Sent password reset request to {}".format(form.email.data),
              "success")

        return redirect(url_for('home.page'))
    return render_template('reset.html', form=form)

@login.route('/reset/<token>', methods=["GET", "POST"])
@require_unauthed
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.commit()

        flash("Successfully reset password!", "success")
        
        return redirect(url_for('login.page'))

    return render_template('reset_with_token.html', form=form, token=token)
