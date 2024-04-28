from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Word
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # providing the schema for the note
            db.session.add(new_note)  # adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

        word_data = request.json
        if word_data:
            word = word_data.get('word')
            translation = word_data.get('translation')

            if len(word) < 1:
                flash('Word is too short!', category='error')
            else:
                new_word = Word(word=word, translation=translation, user_id=current_user.id)
                db.session.add(new_word)
                db.session.commit()
                flash('Word added!', category='success')

    return render_template("home2.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/add-word', methods=['POST'])
def add_word():
    data = request.get_json()
    if data:
        try:
            new_word = Word(word=data['word'], translation=data['translation'],sentence=data['sentence'], user_id=current_user.id)
            # handle other fields and save to db
            db.session.add(new_word)
            db.session.commit()
            return jsonify({'success':True, 'word': new_word.word, 'translation':new_word.translation, 'sentence':new_word.sentence})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'Invalid data'}), 400

@views.route('/get-user-data', methods=['GET'])
@login_required
def get_user_data():
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    words = Word.query.filter_by(user_id=current_user.id).all()

    user_data = {'words': [{'word':word.word, 'translation':word.translation, 'sentence':word.sentence} for word in words]}
    return jsonify(user_data)