import os, requests
from flask import Flask, redirect
from analyzer.analyzer_routes import analyzer_bp
from users.users_routes import users_bp  # Add this line

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
app.register_blueprint(analyzer_bp)
app.register_blueprint(users_bp)  # Add this line

@app.route('/')
def index():
    return redirect('/analyze')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)