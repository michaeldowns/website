import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = 12

    # Mail
    MAIL_PREFIX = "[Website] "
    MAIL_ADMIN = os.environ.get("MAIL_ADMIN")

    # Captchas
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
    RECAPTCHA_DATA_ATTRS = {'align': 'center', 'margin': 'auto'}

    # Website settings
    USERNAME_LENGTH = 16
    EMAIL_LENGTH = 64
    PASSWORD_LENGTH = 128


class DevelopmentConfig(Config):
    DEBUG = True

    # Mail
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SENDER = "{}@gmail.com".format(MAIL_USERNAME)
    

    # Database
    db_username = "postgres"
    db_server = "localhost"
    db_name = "website"
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "postgresql://{}@{}/{}".format(db_username,
                                                             db_server,
                                                             db_name)


class TestingConfig(Config):
    TESTING = True
    

class ProductionConfig(Config):
    pass




