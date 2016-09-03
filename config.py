class Config(object):
    DEBUG = False
    TESTING = False
    DB_STRING = 'dbname=naas user=postgres host=localhost'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    LOGGER_HANDLER_POLICY = 'never'
    DB_STRING = 'dbname=testdb user=postgres host=localhost'
