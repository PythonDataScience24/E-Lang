from exts import db

class LanguageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(500), nullable=False)
    translation = db.Column(db.String(500), nullable=False)
    sentence = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<LanguageModel {self.word}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, word, translation, sentence, difficulty):
        self.word = word
        self.translation = translation
        self.sentence = sentence
        self.difficulty = difficulty
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    vocabularies = db.relationship("Vocabulary", backref="user", lazy=True)
    quizzes = db.relationship("Quiz", backref="user", lazy=True)
    progress = db.relationship("Progress", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class SentencePair(db.Model):
    __tablename__ = 'sentence_pairs'
    id = db.Column(db.Integer, primary_key=True)
    english_sentence = db.Column(db.String(255), nullable=False)
    german_sentence = db.Column(db.String(255), nullable=False)
    correct_word = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<SentencePair {self.english_sentence} - {self.german_sentence}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, english_sentence, german_sentence, correct_word):
        self.english_sentence = english_sentence
        self.correct_word = correct_word
        self.german_sentence = german_sentence
        db.session.commit()


class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    vocab_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    pronunciation = db.Column(db.String(100))
    example_usage = db.Column(db.Text)
    category = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)
    quiz_questions = db.relationship('QuizQuestion', backref='vocabulary', lazy=True)
    progress_entries = db.relationship('Progress', backref='vocabulary', lazy=True)


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    vocab_id = db.Column(db.Integer, db.ForeignKey('vocabulary.vocab_id'), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text)
    responses = db.relationship('UserResponse', backref='quiz_question', lazy=True)


class UserResponse(db.Model):
    __tablename__ = 'user_responses'
    response_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.question_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, nullable=False)


class Progress(db.Model):
    __tablename__ = 'progress'
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vocab_id = db.Column(db.Integer, db.ForeignKey('vocabulary.vocab_id'), nullable=False)
    date_practiced = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Progress user_id={self.user_id} vocab_id={self.vocab_id}>"
