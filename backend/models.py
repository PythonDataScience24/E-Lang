from exts import db


"""
class LanguageModel():
    id : int primary key
    word:str
    translation:str
    sentence: str(text)
    difficulty: int
    phonetics: blob
    
"""

class LanguageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(500), nullable=False)
    translation = db.Column(db.String(500), nullable=False)
    sentence = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<LanguageModel{self.word}>"

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




"""
class User:
    id : int primary key
    username : str
    password : str       
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User{self.username}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
