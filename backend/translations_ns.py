from flask_restx import Resource, fields, Namespace
from flask import jsonify, request
import random
import requests
import copy
import string
from models import SentencePair

# Initialize pipelines and seed
target_lang: str = 'deu'
source_lang: str = 'eng'
request_url: str = "https://tatoeba.org/eng/api_v0/search"

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
def remove_punctuation(word: str) -> str:
    for punc_char in string.punctuation:
        word = word.replace(punc_char, '')
    return word


def generate_sentences():
    url: str = copy.copy(request_url)
    url += "?from="+target_lang
    url += "&to="+source_lang
    url += "&sort=random"
    seed: int = random.randint(0, 30000)
    url += "&rand_seed="+str(seed)  # so we get different sentences every time
    url += "&orphan=no"
    url += "&unapproved=no"  # site says those are "likely to be incorrect"
    url += "&word_count_max=15"
    url += "&word_count_min=3"
    req = requests.get(url)
    req_parsed = req.json()
    first_sentence = req_parsed['results'][0]
    target_text = first_sentence['text']
    translation_categories = first_sentence['translations']
    # print(first_sentence)
    for category in translation_categories:
        if len(category) != 0:
            for translation in category:
                if len(translation) != 0:
                    source_text = translation['text']
    return target_text, source_text


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
        translation, english_sentence = generate_sentences()
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
        translation, english_sentence = generate_sentences()
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

        user_input_compare = remove_punctuation(user_input.strip().lower())
        correct_compare = remove_punctuation(correct_word.strip().lower())

        if user_input_compare == correct_compare:
            return {"message": "Correct! Well done."}, 200
        else:
            return {"message": "Incorrect! Try again."}, 400
