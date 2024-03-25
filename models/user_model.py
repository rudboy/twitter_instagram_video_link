from app import db
from sqlalchemy import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    token = db.Column(db.String(), nullable=False)
    listVideo = db.Column(ARRAY(db.JSON), nullable=True)


    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, email={self.email}, token={self.token}, listVideo={self.listVideo}>'

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "token": self.token,
            "listVideo": self.listVideo
        }
