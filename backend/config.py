from decouple import config
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class Config:
    """
    Base configuration class with default settings.
    """
    SECRET_KEY = config('SECRET_KEY')
    # Line split for PEP8 compliance
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS',
                                            cast=bool)


class DevConfig(Config):
    """
    Development configuration class.
    Inherits from the base Config class.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    """
    Production configuration class.
    Inherits from the base Config class.
    """
    pass


# Blank line above added for PEP8 compliance
class TestConfig(Config):
    """
    Testing configuration class.
    Inherits from the base Config class.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    TESTING = True

