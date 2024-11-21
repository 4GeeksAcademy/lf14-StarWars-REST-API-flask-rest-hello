from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_character = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    user_planet = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user = db.relationship('User')
    character = db.relationship('Character')
    planet = db.relationship('Planet')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_character": self.user_character,
            "user_planet": self.user_planet
        }