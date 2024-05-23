from flask_restx import Resource, fields, Namespace
from flask import jsonify, request
import requests
import random
import copy
import string
from exts import db
from models import Quiz, QuizQuestion, UserResponse, Progress, SentencePair, Vocabulary

# Initialize the RNG (for consistency)
random.seed(42)
target_lang = 'deu'
source_lang = 'eng'
request_url = "https://tatoeba.org/eng/api_v0/search"

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
    "user_input": fields.String(required=True, description="User provided word"),
    "question_id": fields.Integer(required=True, description="ID of the question being answered")
})

# Helper functions
def remove_punctuation(word: str) -> str:
    for punc_char in string.punctuation:
        word = word.replace(punc_char, '')
    return word

def create_gap_sentence(translation: str):
    words = translation.split()
    gap_index = random.randint(0, len(words) - 1)
    correct_word = words[gap_index]
    words[gap_index] = '_____'
    return ' '.join(words), correct_word

def generate_sentences(vocab_word):
    url = copy.copy(request_url)
    url += "?from=" + target_lang
    url += "&to=" + source_lang
    url += "&sort=random"
    seed = random.randint(0, 30000)
    url += "&rand_seed=" + str(seed)  # so we get different sentences every time
    url += "&orphan=no"
    url += "&unapproved=no"  # site says those are "likely to be incorrect"
    url += "&word_count_max=15"
    url += "&word_count_min=3"
    url += f"&query={vocab_word}"
    req = requests.get(url)
    req_parsed = req.json()
    first_sentence = req_parsed['results'][0]
    target_text = first_sentence['text']
    translation_categories = first_sentence['translations']
    for category in translation_categories:
        if len(category) != 0:
            for translation in category:
                if len(translation) != 0:
                    source_text = translation['text']
                    return target_text, source_text
    return None, None

# Class-based Resource for generating sentences
@translations_ns.route('/generate_sentence')
class SentenceGenerator(Resource):
    def get(self):
        vocab_word = request.args.get('vocab_word')
        if not vocab_word:
            return jsonify({"message": "Vocab word is required"}), 400

        german_sentence, english_sentence = generate_sentences(vocab_word)
        if german_sentence and english_sentence:
            gap_sentence, correct_word = create_gap_sentence(german_sentence)
            return jsonify({
                'english_sentence': english_sentence,
                'german_sentence': gap_sentence,
                'correct_word': correct_word
            })
        else:
            return jsonify({"message": "Could not generate sentences"}), 500

# Class-based Resource for translations
@translations_ns.route('/translations')
class Translations(Resource):
    @translations_ns.expect(translations_model)
    @translations_ns.marshal_with(translations_model)
    def get(self):
        vocab_word = request.args.get('vocab_word')
        if not vocab_word:
            return jsonify({"message": "Vocab word is required"}), 400

        german_sentence, english_sentence = generate_sentences(vocab_word)
        if german_sentence and english_sentence:
            gap_sentence, correct_word = create_gap_sentence(german_sentence)
            return {
                'english_sentence': english_sentence,
                'german_sentence': gap_sentence,
                'correct_word': correct_word
            }
        else:
            return {"message": "Could not generate sentences"}, 500

# Class-based Resource for creating a quiz
@translations_ns.route('/create_quiz')
class CreateQuiz(Resource):
    def post(self):
        user_id = request.json.get('user_id')
        if not user_id:
            return {"message": "User ID is required"}, 400

        new_quiz = Quiz(user_id=user_id)
        db.session.add(new_quiz)
        db.session.commit()

        return {"quiz_id": new_quiz.quiz_id}, 201

# Class-based Resource for adding questions to a quiz
@translations_ns.route('/add_question')
class AddQuestion(Resource):
    def post(self):
        quiz_id = request.json.get('quiz_id')
        if not quiz_id:
            return {"message": "Quiz ID is required"}, 400

        # Fetch a random vocabulary word from the user's vocabulary
        vocab = Vocabulary.query.filter_by(user_id=quiz_id).order_by(db.func.random()).first()
        if not vocab:
            return {"message": "No vocabulary found for this user"}, 404

        german_sentence, english_sentence = generate_sentences(vocab.word)
        if not german_sentence or not english_sentence:
            return {"message": "Could not generate sentences"}, 500

        gap_sentence, correct_word = create_gap_sentence(german_sentence)

        new_question = QuizQuestion(
            quiz_id=quiz_id,
            question_type='fill-in-the-blank',
            vocab_id=vocab.vocab_id
        )
        db.session.add(new_question)
        db.session.commit()

        # Save correct answer for validation
        new_sentence_pair = SentencePair(
            german_sentence=german_sentence,
            english_sentence=english_sentence,
            correct_word=correct_word
        )
        db.session.add(new_sentence_pair)
        db.session.commit()

        return {
            'quiz_id': quiz_id,
            'question_id': new_question.question_id,
            'german_sentence': gap_sentence,
            'english_sentence': english_sentence,
            'correct_word': correct_word
        }, 201

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
        question_id = data.get('question_id')

        if not user_input or not question_id:
            return {"message": "Required data missing"}, 400

        # Fetch the question and correct word
        question = QuizQuestion.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        correct_word = SentencePair.query.filter_by(german_sentence=question.german_sentence).first().correct_word

        is_correct = remove_punctuation(user_input.strip().lower()) == remove_punctuation(correct_word.strip().lower())

        new_response = UserResponse(
            question_id=question_id,
            user_id=question.quiz.user_id,
            user_answer=user_input,
            is_correct=is_correct
        )
        db.session.add(new_response)
        db.session.commit()

        return {"message": "Correct! Well done."} if is_correct else {"message": "Incorrect! Try again."}

# Class-based Resource for tracking progress
@translations_ns.route('/progress')
class ProgressTracker(Resource):
    def post(self):
        user_id = request.json.get('user_id')
        vocab_id = request.json.get('vocab_id')
        score = request.json.get('score')

        if not user_id or not vocab_id or not score:
            return {"message": "Required data missing"}, 400

        new_progress = Progress(
            user_id=user_id,
            vocab_id=vocab_id,
            score=score
        )
        db.session.add(new_progress)
        db.session.commit()

        return {"message": "Progress recorded successfully"}, 201
