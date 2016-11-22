import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = '\xe6\xb5\x95Z\xbb\xe9\x05\xf2%\x87T\xbf5\xc3\xfb!\x94\xaf\x7f\xdc\x8b\x9e\xa1\x19'
    DEBUG = False


class DevelopementConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thermos.db')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thermos.db')


config_by_name = dict(dev = DevelopementConfig,
                      test = TestingConfig,
                      prod = ProductionConfig
                     )