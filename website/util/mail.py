from threading import Thread

from flask.ext.mail import Message

from .. import app, mail

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, html):
    msg = Message(app.config['MAIL_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'],
                  recipients=[to])
    msg.html = html

    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

    return thr
    
if __name__ == "__main__":
    with app.app_context():
        send_email("michaeldowns15@gmail.com", "subject", "test")
