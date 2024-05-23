from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Namespace, Resource, fields
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, LanguageModel, Vocabulary, Progress, User, Quiz, QuizQuestion, UserResponse
import pandas as pd
import matplotlib.pyplot as plt
import io, os
import spacy
from transformers import pipeline, set_seed
import requests
import random
import copy
import string

# Model the Namespaces to Use
language_ns = Namespace('language_ns', description='Namespace for Getting Language and words')
vocabulary_ns = Namespace('vocabulary_ns', description='Namespace for Managing Vocabulary')
quiz_ns = Namespace('quiz_ns', description='Namespace for Managing Quizzes')

set_seed(100)
translator = pipeline('translation_en_to_de', model='Helsinki-NLP/opus-mt-en-de')

# Speech Tagging
nlp = spacy.load('de_core_news_sm')

# Load the Deutsch word frequency data
current_dir = os.path.dirname(__file__)
deutsch_df = pd.read_excel(os.path.join(current_dir, 'Deutschwords', 'Deutsch.xlsx'))

# Dictionary to Speed lookup of words based on frequency
word_freq_de = pd.Series(deutsch_df.WFfreqcount.values, index=deutsch_df.Word).to_dict()

target_lang = 'deu'
source_lang = 'eng'
request_url = "https://tatoeba.org/eng/api_v0/search"


# Rating word based on difficulty
def rate_difficulty(word):
    if word in word_freq_de:
        freq = word_freq_de.get(word.lower(), 0)
        if freq > 10000:
            return 1  # Easy word
        elif freq > 5000:
            return 2  # Medium Hard
        elif freq > 1000:
            return 3  # Medium Hard
        elif freq > 500:
            return 4  # Medium Hard
        else:
            return 5  # Hard
    else:
        return 5  # New word


# Categorize user word
def categorize_word(word):
    doc = nlp(word)
    if doc:
        return doc[0].pos_
    else:
        return "UNKNOWN"


# Validate User word
def validate_translation(word, translation):
    # Should check word vs models translation
    return True  # Assumes all translations are true


def remove_punctuation(word):
    for punc_char in string.punctuation:
        word = word.replace(punc_char, '')
    return word


def create_gap_sentence(translation):
    words = translation.split()
    gap_index = random.randint(0, len(words) - 1)
    correct_word = words[gap_index]
    words[gap_index] = '_____'
    return ' '.join(words), correct_word


def generate_sentences():
    url = copy.copy(request_url)
    url += "?from=" + target_lang
    url += "&to=" + source_lang
    url += "&sort=random"
    seed = random.randint(0, 30000)
    url += "&rand_seed=" + str(seed)
    url += "&orphan=no"
    url += "&unapproved=no"
    url += "&word_count_max=15"
    url += "&word_count_min=3"
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


# Serialize the Classes (Expose model as JSON)
language_model = language_ns.model(
    'LanguageModel',
    {
        "id": fields.Integer(),
        "word": fields.String(),
        "translation": fields.String(),
        "sentence": fields.String(),
        "difficulty": fields.Integer()
    }
)

vocabulary_model = vocabulary_ns.model(
    'VocabularyModel',
    {
        'vocab_id': fields.Integer(),
        'user_id': fields.Integer(),
        'word': fields.String(),
        'translation': fields.String(),
        'pronunciation': fields.String(),
        'example_usage': fields.String(),
        'category': fields.String(),
        'difficulty': fields.Integer()
    }
)

quiz_model = quiz_ns.model(
    'QuizModel',
    {
        'quiz_id': fields.Integer(),
        'user_id': fields.Integer(),
        'date_created': fields.DateTime(),
        'questions': fields.List(fields.Nested(vocabulary_model))
    }
)
quiz_question_model = quiz_ns.model(
    'QuizQuestionModel',
    {
        'question_id': fields.Integer(),
        'quiz_id': fields.Integer(),
        'vocab_id': fields.Integer(),
        'question_type': fields.String(),
        'question': fields.String(),
        'correct_word': fields.String()  # Add correct_word to the model if you need it in the response
    }
)


@language_ns.route('/languagemodel')
class LanguagesResource(Resource):
    @language_ns.marshal_list_with(language_model)
    def get(self):
        all_words = LanguageModel.query.all()
        return all_words

    @language_ns.marshal_with(language_model)
    @language_ns.expect(language_model)
    def post(self):
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
        one_word = LanguageModel.query.get_or_404(id)
        return one_word

    @language_ns.marshal_with(language_model)
    def put(self, id):
        word_to_update = LanguageModel.query.get_or_404(id)
        data = request.get_json()
        word_to_update.update(data.get('word'), data.get('translation'),
                              data.get('sentence'), data.get('difficulty'))
        return word_to_update, 200

    @language_ns.marshal_with(language_model)
    def delete(self, id):
        word_to_delete = LanguageModel.query.get_or_404(id)
        word_to_delete.delete_from_db()
        return '', 204


@vocabulary_ns.route('/vocabulary/<int:vocab_id>')
class VocabularyResource(Resource):
    @vocabulary_ns.marshal_with(vocabulary_model)
    def get(self, vocab_id):
        """Get a single vocabulary entry"""
        vocab = Vocabulary.query.get_or_404(vocab_id)
        return vocab

    @vocabulary_ns.marshal_with(vocabulary_model)
    def put(self, vocab_id):
        """Update a vocabulary entry"""
        data = request.json
        vocab = Vocabulary.query.get_or_404(vocab_id)
        vocab.word = data['word']
        vocab.translation = data['translation']
        vocab.pronunciation = data.get('pronunciation', vocab.pronunciation)
        vocab.example_usage = data.get('example_usage', vocab.example_usage)
        vocab.category = data.get('category', vocab.category)
        vocab.difficulty = data.get('difficulty', vocab.difficulty)
        db.session.commit()
        return vocab, 200

    def delete(self, vocab_id):
        """Delete a vocabulary entry"""
        vocab = Vocabulary.query.get_or_404(vocab_id)
        db.session.delete(vocab)
        db.session.commit()
        return '', 204


@language_ns.route('/progress/detailed/<int:user_id>/visualization')
class ProgressVisualizationResource(Resource):
    def get(self, user_id):
        progress_entries = Progress.query.filter_by(user_id=user_id).all()
        if not progress_entries:
            return jsonify({"message": "No progress data found for this user"}), 404

        data = [{
            'word': entry.vocabulary.word,
            'date_practiced': entry.date_practiced,
            'score': entry.score
        } for entry in progress_entries]

        df = pd.DataFrame(data)
        avg_scores = df.groupby('word')['score'].mean().reset_index()
        practice_counts = df.groupby('word')['score'].count().reset_index().rename(columns={'score': 'practice_count'})
        progress_df = pd.merge(avg_scores, practice_counts, on='word')

        fig, ax1 = plt.subplots(figsize=(10, 6))
        color = 'tab:blue'
        ax1.set_xlabel('Word')
        ax1.set_ylabel('Average Score', color=color)
        ax1.bar(progress_df['word'], progress_df['score'], color=color, alpha=0.6, label='Average Score')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_xticklabels(progress_df['word'], rotation=45, ha='right')

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Practice Count', color=color)
        ax2.plot(progress_df['word'], progress_df['practice_count'], color=color, marker='o', label='Practice Count')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.title(f'Progress Report for User ID {user_id}')
        plt.legend(loc='upper left')

        # Save plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='progress_report.png')


@language_ns.route('/progress/analysis/<int:user_id>')
class ProgressAnalysisResource(Resource):
    def get(self, user_id):
        progress_entries = Progress.query.filter_by(user_id=user_id).all()
        if not progress_entries:
            return jsonify({"message": "No progress data found for this user"}), 404

        data = [{
            'word': entry.vocabulary.word,
            'date_practiced': entry.date_practiced.strftime('%Y-%m-%d %H:%M:%S'),
            'score': entry.score
        } for entry in progress_entries]

        df = pd.DataFrame(data)

        # Calculate overall statistics
        total_practices = len(df)
        average_score = df['score'].mean()
        max_score = df['score'].max()
        min_score = df['score'].min()
        std_dev = df['score'].std()

        # Calculate performance per word
        performance_per_word = df.groupby('word')['score'].agg(['mean', 'count']).reset_index()
        performance_per_word.rename(columns={'mean': 'average_score', 'count': 'practice_count'}, inplace=True)

        analysis_summary = {
            'total_practices': total_practices,
            'average_score': average_score,
            'max_score': max_score,
            'min_score': min_score,
            'std_dev': std_dev,
            'performance_per_word': performance_per_word.to_dict(orient='records')
        }

        return jsonify(analysis_summary)


@vocabulary_ns.route('/vocabulary')
class VocabularyListResource(Resource):
    @vocabulary_ns.marshal_list_with(vocabulary_model)
    @jwt_required()
    def get(self):
        """Get all vocabulary entries for the current user"""
        user_id = get_jwt_identity()
        vocab_list = Vocabulary.query.filter_by(user_id=user_id).all()
        return vocab_list

    @vocabulary_ns.expect(vocabulary_model, validate=True)
    @vocabulary_ns.marshal_with(vocabulary_model)
    @jwt_required()
    def post(self):
        """Add a new vocabulary entry"""
        user_id = get_jwt_identity()
        data = request.json

        print("Received payload:", data)  # Log the received payload

        word = data.get('word')
        translation = data.get('translation')
        pronunciation = data.get('pronunciation')
        example_usage = data.get('example_usage')

        if not word:
            return jsonify({"message": "Word is required."}), 422
        if not translation:
            return jsonify({"message": "Translation is required."}), 422
        if not pronunciation:
            return jsonify({"message": "Pronunciation is required."}), 422
        if not example_usage:
            return jsonify({"message": "Example usage is required."}), 422

        # Categorize the word
        category = categorize_word(word)

        # Rate the difficulty
        difficulty = rate_difficulty(translation)

        new_vocab = Vocabulary(
            user_id=user_id,
            word=word,
            translation=translation,
            pronunciation=pronunciation,
            example_usage=example_usage,
            category=category,
            difficulty=difficulty
        )
        db.session.add(new_vocab)
        db.session.commit()
        return new_vocab, 201


@quiz_ns.route('/generate')
class QuizGenerationResource(Resource):
    @jwt_required()
    @quiz_ns.marshal_with(quiz_question_model)
    def post(self):
        user_id = get_jwt_identity()
        vocab_list = Vocabulary.query.filter_by(user_id=user_id).all()

        if not vocab_list:
            return {"message": "No vocabulary found for this user."}, 404

        vocab_item = random.choice(vocab_list)
        word = vocab_item.word
        translation = vocab_item.translation

        german_sentence, english_sentence = generate_sentences()
        if not german_sentence:
            return {"message": "Could not generate sentences."}, 500

        gap_sentence, correct_word = create_gap_sentence(german_sentence)

        # Add the new word to the vocabulary with the generated sentence as an example of use
        new_vocab = Vocabulary(
            user_id=user_id,
            word=word,
            translation=translation,
            pronunciation='',  # Add pronunciation if available
            example_usage=german_sentence,
            category=categorize_word(word),
            difficulty=rate_difficulty(translation)
        )
        db.session.add(new_vocab)
        db.session.commit()

        new_quiz = Quiz(user_id=user_id)
        db.session.add(new_quiz)
        db.session.commit()

        new_question = QuizQuestion(
            quiz_id=new_quiz.quiz_id,
            vocab_id=new_vocab.vocab_id,
            question_type="gap_fill",
            question=gap_sentence
        )
        db.session.add(new_question)
        db.session.commit()

        response_data = {
            'question_id': new_question.question_id,
            'quiz_id': new_quiz.quiz_id,
            'vocab_id': new_vocab.vocab_id,
            'question_type': "gap_fill",
            'question': gap_sentence,
            'correct_word': correct_word  # Include correct_word if needed
        }

        return response_data, 201


@quiz_ns.route('/<int:quiz_id>')
class QuizResource(Resource):
    @quiz_ns.marshal_with(quiz_model)
    def get(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        return quiz


@quiz_ns.route('/submit/<int:quiz_id>')
class QuizSubmissionResource(Resource):
    @jwt_required()
    def post(self, quiz_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        for response in data.get('responses', []):
            question_id = response.get('question_id')
            user_answer = response.get('user_answer')

            question = QuizQuestion.query.get_or_404(question_id)
            correct_word = Vocabulary.query.get_or_404(question.vocab_id).word

            is_correct = (user_answer.lower() == correct_word.lower())

            user_response = UserResponse(
                question_id=question_id,
                user_id=user_id,
                user_answer=user_answer,
                is_correct=is_correct
            )
            db.session.add(user_response)

            # Update progress
            progress = Progress(
                user_id=user_id,
                vocab_id=question.vocab_id,
                score=1 if is_correct else 0
            )
            db.session.add(progress)

        db.session.commit()

        return jsonify({"message": "Quiz submitted successfully."}), 200
