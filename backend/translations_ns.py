from flask_restx import Resource, fields, Namespace
from flask import jsonify, request
from transformers import pipeline, set_seed
import random
import re
from models import SentencePair

# Initialize pipelines and seed
set_seed(42)
text_generator = pipeline('text-generation', model='gpt2')
translator = pipeline('translation_en_to_de',
                      model='Helsinki-NLP/opus-mt-en-de')

# Define the namespace
translations_ns = Namespace('translations_ns',
                            description='Namespace for Getting Sentence Translations')

# Serialization schema
translations_model = translations_ns.model(
    'Translations',
    {
        "id": fields.Integer(),
        "german_sentence": fields.String(),
        "english_sentence": fields.String(),
        "correct_word": fields.String()
    }
)

# This model will just involve the necessary fields for validation
translations_model_1 = translations_ns.model('Validation', {
    "user_input": fields.String(required=True, description="User provided word")
})


# Helper functions
def generate_english_sentence():
    while True:
        generated_text = text_generator("This is", max_length=20, num_return_sequences=1)[0]['generated_text'].strip()
        sentences = re.split(r'[.?!]', generated_text)
        for sentence in sentences:
            words = sentence.strip().split()
            if 3 <= len(words) <= 10:
                return ' '.join(words)


def create_gap_sentence(translation):
    words = translation.split()
    gap_index = random.randint(0, len(words) - 1)
    correct_word = words[gap_index]
    words[gap_index] = '_____'
    return ' '.join(words), correct_word


# Class-based Resource for generating sentences
@translations_ns.route('/generate_sentence')
class SentenceGenerator(Resource):
    def get(self):
        english_sentence = generate_english_sentence()
        translation = translator(english_sentence)[0]['translation_text']
        gap_sentence, correct_word = create_gap_sentence(translation)
        return jsonify({
            'english_sentence': english_sentence,
            'german_sentence': gap_sentence,
            'correct_word': correct_word
        })


# Class-based Resource for translations
@translations_ns.route('/translations')
class Translations(Resource):
    @translations_ns.expect(translations_model)
    @translations_ns.marshal_with(translations_model)
    def get(self):
        english_sentence = generate_english_sentence()
        translation = translator(english_sentence)[0]['translation_text']
        gap_sentence, correct_word = create_gap_sentence(translation)
        return {
            'english_sentence': english_sentence,
            'german_sentence': gap_sentence,
            'correct_word': correct_word
        }


# Class-based Resource for answer validation
@translations_ns.route('/validate')
class AnswerValidator(Resource):
    @translations_ns.marshal_with(translations_model_1)
    @translations_ns.expect(translations_model_1)
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400

        user_input = data.get('user_input')
        correct_word = data.get('correct_word')

        if not user_input or not correct_word:
            return {"message": "Required data missing"}, 400

        if user_input.strip().lower() == correct_word.strip().lower():
            return {"message": "Correct! Well done."}, 200
        else:
            return {"message": "Incorrect! Try again."}, 400
