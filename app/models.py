from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Image(db.Model):
    """Table to hold links to URLs for each picture"""
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe = relationship("Recipe", back_populates="images")
    filename = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, nullable=True)

class Recipe(db.Model):
    """Details on recipe"""
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    id_recipe_category = db.Column(db.Integer, db.ForeignKey('category.id'))
    recipe_category = relationship("RecipeCategory", back_populates="recipes")
    source_type = db.Column(db.String(8), index=True)
    web_link = db.Column(db.Text, nullable=True)
    book_title = db.Column(db.String(120), index=True, nullable=True)
    book_page = db.Column(db.Integer, nullable=True)
    book_image_path = db.Column(db.String(256), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    images = relationship("Image", back_populates="recipe")

class RecipeCategory(db.Model):
    """Categories to sort Recipes into"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    recipes = relationship("Recipe", back_populates="recipe_category")

    def __repr__(self):
        return '<RecipeCategory {}>'.format(self.name)