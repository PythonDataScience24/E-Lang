from main import create_app

from config import DevConfig, TestConfig

if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()
