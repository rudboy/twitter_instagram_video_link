from flask import Flask, jsonify, request
import json
from instaDownload import download_media
from twitterDownload import api_twitter

from urllib.parse import urlparse

app = Flask(__name__)

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
        if token == "67856767KUTUYGY6RYTEYER476558H87GGGFFHFDHGFDYTRET54Y575YVRCDYGRCDVYTEZET34ZY54R8T9T":  # Votre logique de validation de jeton ici
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Token invalide'}), 401

    # Renomme la fonction wrapper pour garder le nom de la fonction d'origine
    wrapper.__name__ = f.__name__
    return wrapper

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
# @verifier_token
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
    # app.run(port=4000)
    app.run(debug=True)
