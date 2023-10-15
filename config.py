import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CUSTOM_BUILT_MODEL_ID=os.environ.get("CUSTOM_BUILT_MODEL_ID")
    CONTAINER_SAS_URL=os.environ.get("CONTAINER_SAS_URL")
    AZURE_FORM_RECOGNIZER_ENDPOINT=os.environ.get("AZURE_FORM_RECOGNIZER_ENDPOINT")
    AZURE_FORM_RECOGNIZER_KEY=os.environ.get("AZURE_FORM_RECOGNIZER_KEY")

    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_MATCHMAKING') or \
        'sqlite:///' + os.path.join(basedir, 'matchmaking_db.sqlite')
    SQLALCHEMY_BINDS = {
        'learning_path': os.environ.get('DATABASE_URI_LEARNINGPATH') or \
            'sqlite:///' + os.path.join(basedir, 'learning_path_db.sqlite')
    }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_MATCHMAKING')
    SQLALCHEMY_BINDS = {
        'learning_path': os.environ.get('DATABASE_URI_LEARNINGPATH')
    }


class QualityAssuranceConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_MATCHMAKING')
    SQLALCHEMY_BINDS = {
        'learning_path': os.environ.get('DATABASE_URI_LEARNINGPATH')
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_MATCHMAKING')
    SQLALCHEMY_BINDS = {
        'learning_path': os.environ.get('DATABASE_URI_LEARNINGPATH')
    }


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'quality': QualityAssuranceConfig,
    'default': DevelopmentConfig
}
