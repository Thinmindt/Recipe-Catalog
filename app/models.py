from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Recipe(db.Model):
    """Details on recipe"""
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    type = db.Column(db.String(8), index=True)
    web_link = db.Column(db.Text, nullable=True)
    book_title = db.Column(db.String(120), index=True, nullable=True)
    book_page = db.Column(db.Integer, nullable=True)
    book_image_path = db.Column(db.String(256), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    