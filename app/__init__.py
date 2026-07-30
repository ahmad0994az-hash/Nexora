from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "<h1>🚀 Welcome to Nexora!</h1><p>The project has started successfully.</p>"

    return app
