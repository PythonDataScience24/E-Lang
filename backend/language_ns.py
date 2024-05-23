from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Namespace, Resource, fields
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, LanguageModel, Vocabulary, Progress
import pandas as pd
import matplotlib.pyplot as plt
import io, os
import spacy
from transformers import pipeline, set_seed

# Initialize pipelines and set seed
set_seed(100)
translator = pipeline('translation_en_to_de', model='Helsinki-NLP/opus-mt-en-de')

# For speech tagging
nlp = spacy.load('de_core_news_sm')

# Load the Deutsch word frequency data
current_dir = os.path.dirname(__file__)
deutsch_df = pd.read_excel(os.path.join(current_dir, 'Deutschwords', 'Deutsch.xlsx'))

# Create dictionary to speed lookup of words based on frequency
word_freq_de = pd.Series(deutsch_df.WFfreqcount.values, index=deutsch_df.Word).to_dict()

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

language_ns = Namespace('language_ns', description='Namespace for Getting Language and words')
vocabulary_ns = Namespace('vocabulary_ns', description='Namespace for Managing Vocabulary')

# Serialize our class (Expose model as JSON)
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

@language_ns.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello World!'})

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
    def put(self, id):
        """Update a word selection"""
        word_to_update = LanguageModel.query.get_or_404(id)
        data = request.get_json()
        word_to_update.update(data.get('word'), data.get('translation'),
                              data.get('sentence'), data.get('difficulty'))
        return word_to_update, 200

    @language_ns.marshal_with(language_model)
    def delete(self, id):
        """Delete a word selection"""
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
