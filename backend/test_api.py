import unittest
from main import create_app
from config import TestConfig
from exts import db


class BackendTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)

        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.init_app(self.app)

            db.create_all()

    def test_hello_world(self):
        hello_world_response = self.client.get('/language_ns/hello')

        json = hello_world_response.json
        print(json)

        self.assertEqual(json, {
            "message": "Hello World!"
        })

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
