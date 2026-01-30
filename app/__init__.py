from flask import Flask, render_template
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__)
    
    # Register the webhook blueprint
    app.register_blueprint(webhook)

    app.route('/')
    def index():
        return render_template("index.html")
    
    return app