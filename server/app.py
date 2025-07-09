

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
import os

from models import db, Restaurant, Pizza, RestaurantPizza

# Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# ROUTES

class Home(Resource):
    def get(self):
        return make_response("<h1>Pizza Restaurant API</h1>", 200)

api.add_resource(Home, '/')

class Restaurants(Resource):
    def get(self):
        restaurants = [r.to_dict() for r in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)

api.add_resource(Restaurants, '/restaurants')


class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        # Include associated pizzas
        result = restaurant.to_dict()
        result["pizzas"] = [rp.pizza.to_dict() for rp in restaurant.resturant_pizzas]
        return result, 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204

api.add_resource(RestaurantById, '/restaurants/<int:id>')


class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return pizzas, 200

api.add_resource(Pizzas, '/pizzas')


class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            price = data.get("price")
            pizza_id = data.get("pizza_id")
            restaurant_id = data.get("restaurant_id")

            if not all([price, pizza_id, restaurant_id]):
                return {"errors": ["Missing data"]}, 400

            if not (1 <= price <= 30):
                return {"errors": ["Price must be between 1 and 30"]}, 400

            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)

            if not pizza or not restaurant:
                return {"errors": ["Invalid pizza or restaurant ID"]}, 404

            new_rp = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
            db.session.add(new_rp)
            db.session.commit()

            return pizza.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
