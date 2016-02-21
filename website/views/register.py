from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask.ext.login import current_user

from .. import db
from ..models import User
from ..forms import RegisterForm
from ..util.security import ts
from ..util.mail import send_email
from ..util.decorators import require_unauthed

register = Blueprint('register', __name__)

@register.route('/register', methods=["GET", "POST"])
@require_unauthed
def page():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        
        db.session.add(user)
        db.session.commit()

        # Email confirmation link
        subject = "Confirm your email"

        token = ts.dumps(user.email, salt='email-confirm-key')

        confirm_url = url_for('register.confirm_email', token=token,
                              _external=True)

        html = render_template('email/activate.html', confirm_url=confirm_url)

        send_email(user.email, subject, html)

        flash("Sent confirmation email to {}".format(form.email.data),
              "success")

        return redirect(url_for("home.page"))

    return render_template('register.html', form=form)

@register.route('/confirm/<token>')
@require_unauthed
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(
        email=email
    ).first_or_404()

    user.email_confirmed = True
    db.session.commit()

    flash("Successfuly confirmed {}".format(email), "success")

    return redirect(url_for("login.page"))
