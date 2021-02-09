import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY='ini rahasia'
    ALLOWED_EXTENSIONS = {'bib'}