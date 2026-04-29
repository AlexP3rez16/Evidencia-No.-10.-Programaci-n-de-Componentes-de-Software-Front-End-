from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from controllers.auth import auth_bp
from controllers.libros import libros_bp

app = Flask(__name__)
app.secret_key = 'ducky_secret_2024'

app.register_blueprint(auth_bp)
app.register_blueprint(libros_bp)

if __name__ == '__main__':
    app.run(debug=True)