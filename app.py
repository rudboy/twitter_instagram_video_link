from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os
import json
from urllib.parse import urlparse

from instaDownload import download_media
from twitterDownload import api_twitter

from itsdangerous import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer


load_dotenv()

# Importez l'instance de la base de données depuis database.py
from database import db

# Importez vos routes depuis routes.py
from routes.routes import routes_bp


app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Initialisez la base de données avec l'application Flask
db.init_app(app)

# Enregistrez les routes dans l'application Flask
# app.register_blueprint(routes_bp)

# initialize the app with the extension
with app.app_context():
    db.create_all()
    print('Database created successfully!')

# Fonction pour vérifier le bearer token
def verifier_token(f):
    def wrapper(*args, **kwargs):
        bearer_token = request.headers.get('Authorization')

        # Vérifie si le jeton est présent dans l'en-tête Authorization
        if not bearer_token or not bearer_token.startswith('Bearer '):
            return jsonify({'message': 'Token manquant ou incorrect'}), 401

        # Extrait le jeton du format "Bearer <token>"
        token = bearer_token.split(' ')[1]

        # Supposez ici que vous avez déjà une fonction de validation du token
        # Si le token est valide, appeler la fonction route
        try:
            from models.user_model import User

            user = User.query.filter_by(token=token).first()
            if user is None:
                return jsonify({'error': 'User not found!'}), 404
            serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

            payload = serializer.loads(token,salt=user.email, max_age=3600)

            print(payload)
               # Votre logique de validation de jeton ici
            return f(*args, **kwargs)

        except SignatureExpired:
            return jsonify({'message': 'Token expiré'}), 401

        except BadSignature:
            return jsonify({'message': 'Token invalide'}), 401

    # Renomme la fonction wrapper pour garder le nom de la fonction d'origine
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/')
def index():
    return jsonify({"message": "Welcome to the video downloader api"}), 200

@app.route('/user_singup', methods=['POST'])
def singup():
    from routes.user_route import signUpUser
    json_str = json.dumps(request.json)
    data = json.loads(json_str)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if username is None or email is None or password is None:
        return jsonify({"error": "All fields are required"}), 400
    return signUpUser(username=username, email=email, password=password)

@app.route('/user_login', methods=['POST'])
def login():
    from routes.user_route import loginUser
    json_str = json.dumps(request.json)
    data = json.loads(json_str)
    email = data.get("email")
    password = data.get("password")
    if email is None or password is None:
        return jsonify({"error": "All fields are required"}), 400
    return loginUser(email=email, password=password)

@app.route('/allDelete', methods=['GET'])
def deleteAllTabs():
    from routes.deleteAllTabs_route import deleteAllTabs
    return deleteAllTabs()

# Route pour télécharger les informations de la vidéo Instagram et Twitter
@app.route('/insta_founder', methods=['POST'])
@verifier_token
def get_insta_infos():
    json_str = json.dumps(request.json)
    data = json.loads(json_str)
    url = data.get("url")
    if url is None:
        return jsonify({"error": "URL not found"}), 404

    response = download_media(url)
    if response is None:
        return jsonify({"error": "URL not found"}), 404
    else:
        json_response = json.loads(response)
        return jsonify({"message": "Downloaded successfully","img_url":json_response.get("photoURL"),"video_url":json_response.get("videoURL"),"duration":json_response.get("videoDuration")}), 200

@app.route('/twitter_founder', methods=['POST'])
@verifier_token
def get_twitter_infos():
    json_str = json.dumps(request.json)
    data = json.loads(json_str)
    url = data.get("url")
    if url is None:
        return jsonify({"error": "URL not found"}), 404

    video_url = urlparse(url)
    tweetpath = video_url.path.split('/')
    id = tweetpath[-1]
    json_response = api_twitter(id)
    if json_response is None:
        return jsonify({"error": "URL not found"}), 404
    else:
        return jsonify({"message": "Downloaded successfully","img_url":json_response.get("photoURL"),"video_url":json_response.get("videoURL"),"duration":json_response.get("videoDuration")}), 200

if __name__ == '__main__':
    print("Serever is running...")
    # app.run(port=4000)
    port = int(os.getenv('PORT'))
    app.run(debug=True, port=port)
