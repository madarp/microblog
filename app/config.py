import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db = 'sqlite:///' + os.path.join(basedir, 'app.db')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
