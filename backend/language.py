from models import LanguageModel
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask import request

language_ns = Namespace('language_ns', description='Namespace for Getting Language and words')

# Serialize our class (Expose model as Json)
language_model = language_ns.model(
    'LanguageModel',
    {"id": fields.Integer(),
     "word": fields.String(),
     "translation": fields.String(),
     "sentence": fields.String(),
     "difficulty": fields.Integer()
     }
)


@language_ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello World!'}


@language_ns.route('/languagemodel')
class LanguagesResource(Resource):
    @language_ns.marshal_list_with(language_model)
    def get(self):
        """Get All words and information from database"""
        all_words = LanguageModel.query.all()
        return all_words

    @language_ns.marshal_with(language_model)
    @language_ns.expect(language_model)
    def post(self):
        """Create a new word selection"""
        data = request.get_json()
        new_words = LanguageModel(
            word=data.get("word"),
            translation=data.get("translation"),
            sentence=data.get("sentence"),
            difficulty=data.get("difficulty")
        )

        new_words.save_to_db()
        return new_words, 201


@language_ns.route('/languagemodel/<int:id>')
class LanguageResource(Resource):
    @language_ns.marshal_with(language_model)
    def get(self, id):
        """Get a single word selection"""
        one_word = LanguageModel.query.get_or_404(id)
        return one_word

    @language_ns.marshal_with(language_model)
    @jwt_required()
    def post(self, id):
        """Create a new word selection"""
        word_to_update = LanguageModel.query.get_or_404(id)
        data = request.get_json()

        word_to_update.update(data.get('word'), data.get('translation'), data.get('sentence'), data.get('difficulty'))

        return word_to_update, 201

    @language_ns.marshal_with(language_model)
    @jwt_required()
    def delete(self, id):
        """Delete a word selection"""
        word_to_delete = LanguageModel.query.get_or_404(id)
        word_to_delete.delete_from_db()

        return word_to_delete, 201
