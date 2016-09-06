class Config(object):
    DEBUG = False
    TESTING = False
    DB_STRING = 'dbname=dev user=dev password=dev host=db'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    LOGGER_HANDLER_POLICY = 'never'
    DB_STRING = 'dbname=testdb user=test password=test_password host=db'
