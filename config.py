import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strongkey_secret'
    BLANKSPIDER_ADMIN = os.environ.get('BLANKSPIDER_ADMIN')
    BLANKSPIDER_MAIL_SUBJECT_PREFIX = '[BLANKSPIDER ADMIN]'
    BLANKSPIDER_MAIL_SENDER = 'BLANKSPIDER ADMIN <notification@example.com>'

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True
    MONGO_DATABASE_SERVER = os.environ.get('DEV_DATABASE_SERVER') or 'localhost'
    #MONGO_DATABASE_SERVER = os.environ.get('DEV_DATABASE_SERVER') or '118.107.88.35'
    MONGO_DATABASE_PORT = os.environ.get('DEV_DATABASE_PORT') or 27017
    MONGO_DATABASE_NAME = os.environ.get('DEV_DATABASE_NAME') or 'DEV_BLANKSPIDER'

class Production(Config):
    DEBUG = False
    MONGO_DATABASE_SERVER = os.environ.get('PROD_DATABASE_SERVER') or 'localhost'
    #MONGO_DATABASE_SERVER = os.environ.get('PROD_DATABASE_SERVER') or '118.107.88.35'
    MONGO_DATABASE_PORT = os.environ.get('PROD_DATABASE_PORT') or 27017
    MONGO_DATABASE_NAME = os.environ.get('PROD_DATABASE_NAME') or 'BLANKSPIDER'


config = {
    'development': Development,
    'production': Production,
    'default': Development
}
