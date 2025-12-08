from flask import Flask
from src.routes.chat_blueprint import chat_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(chat_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
