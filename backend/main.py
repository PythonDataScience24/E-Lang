from flask import Flask
from flask_restx import Api
from config import DevConfig
from models import LanguageModel, User, Vocabulary, QuizQuestion, Quiz, UserResponse, Progress
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from auth import auth_ns
from language_ns import language_ns, vocabulary_ns
from flask_cors import CORS
from translations_ns import translations_ns


def create_app():
    config = DevConfig
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    db.init_app(app)

    Migrate(app, db)
    JWTManager(app)

    api = Api(app, title='Language API', version='1.0', description='A simple Language API',doc='/docs')

    api.add_namespace(language_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(translations_ns)
    api.add_namespace(vocabulary_ns)
    # Blank line below added for PEP8 compliance

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'LanguageModel': LanguageModel,
            'User': User,
            'Vocabulary': Vocabulary,
            'QuizQuestion': QuizQuestion,
            'Quiz': Quiz,
            'UserResponse': UserResponse,
            'Progress': Progress
        }

    return app
