import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Extend the base Model class to add common methods
'''


class inheritedClassName(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


'''
Dish with name, price, ingredients
'''
@dataclass
class Dish(inheritedClassName):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    price = Column(Integer)
    ingredient = db.relationship('Ingredient', backref='dish', cascade='all, delete-orphan')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'ingredient': [i.format() for i in self.ingredient]
        }


'''
Ingredients with name, allergen, dish_id
'''
@dataclass
class Ingredient(inheritedClassName):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    allergen = Column(String)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)

    def format(self):
        return {
                'id': self.id,
                'name': self.name,
                'allergen': self.allergen,
                'dish_id': self.dish_id
        }
