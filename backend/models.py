from exts import db

class LanguageModel(db.Model):
    """
    Model for language data.

    Attributes:
        id (int): The primary key.
        word (str): The word.
        translation (str): The translation of the word.
        sentence (str): Example sentence using the word.
        difficulty (int): Difficulty level of the word.
    """
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
    """
    Model for user data.

    Attributes:
        id (int): The primary key.
        username (str): The username.
        password (str): The password.
        vocabularies (Relationship): Vocabulary associated with the user.
        quizzes (Relationship): Quizzes associated with the user.
        progress (Relationship): Progress associated with the user.
    """
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
    """
    Model for sentence pairs.

    Attributes:
        id (int): The primary key.
        english_sentence (str): The English sentence.
        german_sentence (str): The German translation.
        correct_word (str): The correct translation of the word.
    """
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
    """
    Model for vocabulary.

    Attributes:
        vocab_id (int): The primary key.
        user_id (int): The user's ID.
        word (str): The word.
        translation (str): The translation of the word.
        pronunciation (str): The pronunciation of the word.
        example_usage (str): Example usage of the word.
        category (str): The category of the word.
        difficulty (int): Difficulty level of the word.
    """
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
    """
    Model for quiz.

    Attributes:
        quiz_id (int): The primary key.
        user_id (int): The user's ID.
        date_created (datetime): The date when the quiz was created.
    """
    __tablename__ = 'quizzes'
    quiz_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)


class QuizQuestion(db.Model):
    """
    Model for quiz question.

    Attributes:
        question_id (int): The primary key.
        quiz_id (int): The quiz ID.
        vocab_id (int): The vocabulary ID.
        question_type (str): The type of question.
        question (str): The question.
    """
    __tablename__ = 'quiz_questions'
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    vocab_id = db.Column(db.Integer, db.ForeignKey('vocabulary.vocab_id'), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text)
    responses = db.relationship('UserResponse', backref='quiz_question', lazy=True)


class UserResponse(db.Model):
    """
    Model for user response.

    Attributes:
        response_id (int): The primary key.
        question_id (int): The question ID.
        user_id (int): The user ID.
        user_answer (str): The user's answer.
        is_correct (bool): Indicates if the answer is correct.
    """
    __tablename__ = 'user_responses'
    response_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.question_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_answer = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, nullable=False)


class Progress(db.Model):
    """
    Model for progress.

    Attributes:
        progress_id (int): The primary key.
        user_id (int): The user's ID.
        vocab_id (int): The vocabulary ID.
        date_practiced (datetime): The date when the word was practiced.
        score (int): The score obtained for practicing the word.
    """
    __tablename__ = 'progress'
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vocab_id = db.Column(db.Integer, db.ForeignKey('vocabulary.vocab_id'), nullable=False)
    date_practiced = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Progress user_id={self.user_id} vocab_id={self.vocab_id}>"
