from app import db
from flask import jsonify


def deleteAllTabs():
    try:
        db.drop_all()
        return jsonify({'message': 'Delete successfully!'}), 200

    except Exception as e:
        # Autres exceptions non prévues
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500
