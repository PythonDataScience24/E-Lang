import unittest
from main import create_app
from exts import db
from models import User, LanguageModel, Vocabulary, Quiz, QuizQuestion, UserResponse, Progress

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class AuthTestCase(BaseTestCase):
    def test_signup(self):
        response = self.client.post('/auth_ns/signup', json={
            "username": "testuser",
            "password": "password"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User Created Successfully', str(response.data))

    def test_login(self):
        self.client.post('/auth_ns/signup', json={
            "username": "testuser",
            "password": "password"
        })
        response = self.client.post('/auth_ns/login', json={
            "username": "testuser",
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', str(response.data))


class TranslationsTestCase(BaseTestCase):
    def test_generate_sentence(self):
        response = self.client.get('/translations_ns/generate_sentence?vocab_word=test')
        self.assertEqual(response.status_code, 200)
        self.assertIn('english_sentence', str(response.data))
        self.assertIn('german_sentence', str(response.data))
        self.assertIn('correct_word', str(response.data))


class VocabularyTestCase(BaseTestCase):
    def test_add_vocabulary(self):
        self.client.post('/auth_ns/signup', json={
            "username": "testuser",
            "password": "password"
        })
        login_response = self.client.post('/auth_ns/login', json={
            "username": "testuser",
            "password": "password"
        })
        access_token = login_response.json['access_token']

        response = self.client.post('/vocabulary_ns/vocabulary', json={
            "word": "test",
            "translation": "testen",
            "pronunciation": "test-en",
            "example_usage": "This is a test.",
            "category": "noun",
            "difficulty": 1
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('test', str(response.data))


class QuizTestCase(BaseTestCase):
    def test_create_quiz(self):
        self.client.post('/auth_ns/signup', json={
            "username": "testuser",
            "password": "password"
        })
        login_response = self.client.post('/auth_ns/login', json={
            "username": "testuser",
            "password": "password"
        })
        access_token = login_response.json['access_token']

        user = User.query.filter_by(username="testuser").first()

        response = self.client.post('/translations_ns/create_quiz', json={
            "user_id": user.id
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('quiz_id', str(response.data))


if __name__ == '__main__':
    unittest.main()
