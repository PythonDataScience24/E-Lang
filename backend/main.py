from flask import Flask
from flask_restx import Api
from config import DevConfig
from models import LanguageModel, User, Vocabulary, QuizQuestion, Quiz, UserResponse, Progress
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from auth import auth_ns
from sentence_ns import language_ns, vocabulary_ns, quiz_ns
from flask_cors import CORS
from translations_ns import translations_ns
from dash_app import create_dash_app


def create_app():
    config = DevConfig
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app)

    db.init_app(app)

    Migrate(app, db)
    JWTManager(app)

    api = Api(app, title='Language Learning Assistant API', version='1.3', description='API"s For the Backend of Language Learning Assistant',doc='/docs')

    api.add_namespace(language_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(translations_ns)
    api.add_namespace(vocabulary_ns)
    api.add_namespace(quiz_ns)
    # Blank line below added for PEP8 compliance

    #Create Dash App
    dash_app = create_dash_app(app)

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
