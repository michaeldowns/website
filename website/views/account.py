from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user

from .. import db
from ..forms import ChangePasswordForm, ChangeEmailForm
from ..util.security import ts
from ..util.mail import send_email

account = Blueprint('account', __name__)

@account.route('/account', methods=["GET", "POST"])
@login_required
def page():
    password_form = ChangePasswordForm()
    email_form = ChangeEmailForm()

    if password_form.validate_on_submit():
        current_user.password = password_form.new_password.data

        db.session.commit()

        flash("Successfully changed password!", "success")
        
        return redirect(url_for('account.page'))

    if email_form.validate_on_submit():

        subject = "Email change requested"

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(email_form.email.data, salt='recover-key')

        change_url = url_for('account.change_email', token=token,
                                  _external=True)

        html = render_template('email/change.html',
                                   change_url=change_url)

        send_email(email_form.email.data, subject, html)

        flash("Sent email change request to {}".format(email_form.email.data),
              "success")

        return redirect(url_for('account.page'))
    
    
    return render_template('account.html', password_form=password_form,
                           email_form=email_form)

@account.route('/account/change_email/<token>', methods=["GET", "POST"])
@login_required
def change_email(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    current_user.email = email

    db.session.commit()
    
    flash("Successfully changed email!", "success")
        
    return redirect(url_for('account.page'))

    
