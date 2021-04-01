from os import environ


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SECRET_KEY = environ.get('SECRET_KEY')
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    FLASK_ADMIN_SWATCH = 'cerulean'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    # MAIL_PORT = 465
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = False

    # LESS_BIN = '/usr/local/bin/lessc'
    # ASSETS_DEBUG = False
    # ASSETS_AUTO_BUILD = True

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = True

    #Picture uploads
    UPLOAD_FOLDER='app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    #AWS S3 configuration
    S3_BUCKET=environ.get('AWS_BUCKET')
    S3_KEY=environ.get('AWS_ACCESS_KEY_ID')
    S3_SECRET=environ.get('AWS_SECRET_ACCESS_KEY')
    S3_LOCATION= 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    PRODUCTION_DOMAIN = environ.get('PRODUCTION_DOMAIN')

class ProductionConfig(Config):
    TESTING = False
    DEBUG = False

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_BINDS = {
        'eurovision_app':'postgresql:///eurovision_app'
    }


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
