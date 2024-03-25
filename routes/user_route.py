from app import db
from models.user_model import User
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import bcrypt
from itsdangerous.url_safe import URLSafeTimedSerializer
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta


load_dotenv()

def generateToken(email,password):
    try:
        # Créer un serializer avec une clé secrète
        serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
        # Définir la date et l'heure d'expiration
        expiration = datetime.now() + timedelta(hours=1)
        # Créer le payload avec le mot de passe et la date d'expiration
        payload = {'password': password, 'exp': expiration.isoformat()}
        # Générer un token pour l'utilisateur Le token expirera après 1 heure
        token = serializer.dumps(payload, salt=email)
        return token
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500


def signUpUser(username, email, password):

    try:
        hashed_password = bcrypt.hash(password)

        token=generateToken(email,password)

        user = User(username=username, email=email, password=hashed_password, token=token)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!', 'user': user.to_dict()}), 200
    except SQLAlchemyError as e:
        # En cas d'erreur SQLAlchemy (par exemple, violation de contrainte unique)
        db.session.rollback()  # Annuler les changements en cas d'erreur
        return jsonify({'error': 'An error occurred while adding the user.', 'details': str(e)}), 500
    except Exception as e:
        # Autres exceptions non prévues
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500

def loginUser(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'error': 'User not found!'}), 404
        if bcrypt.verify(password, user.password):
            token=generateToken(user.email,user.password)
            user.token=token
            db.session.commit()
            return jsonify({'message': 'User logged in successfully!', 'user': user.to_dict()}), 200
        else:
            return jsonify({'error': 'Incorrect password!'}), 401
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500
