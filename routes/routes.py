from flask import Blueprint , jsonify

# Importez l'instance de la base de données depuis database.py
from database import db

# Créez un Blueprint pour les routes
routes_bp = Blueprint('routes', __name__)

# Importez vos modèles SQLAlchemy ici, par exemple :
from models.user_model import User

# Définissez vos routes Flask ici
@routes_bp.route('/allDelete', methods=['GET'])
def deleteAllTabs():

# Supprimer toutes les tables
    db.drop_all()
    return jsonify({'message': 'User added successfully!'}), 200
