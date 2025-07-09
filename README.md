   Pizza Restaurant API

This is a simple Flask API for managing a pizza restaurant’s menu and pricing. It includes endpoints to view restaurants and pizzas, and to link pizzas to restaurants with custom prices.

This project was built as part of a coding challenge and helped me practice RESTful API design, model relationships in SQLAlchemy, and validation handling.


    Features

  View all restaurants and their info
  View all pizzas
  Add a pizza to a restaurant with a custom price
  Delete a restaurant (along with associated records)
 Validation for price ranges
 Clean error handling

---

 Tech Stack

  Python 3.8
  Flask
  SQLAlchemy
  Flask-Migrate
  SQLite 
  Postman (for testing)

---

    Models

   Restaurant
  `id` (primary key)
  `name`
  `address`
  Has many `RestaurantPizzas` (join table)
  Has many `Pizzas` through `RestaurantPizzas`

     Pizza
  `id` (primary key)
  `name`
 `ingredients`
  Linked to restaurants via `RestaurantPizzas`

    RestaurantPizza
  `id` (primary key)
 `price` (must be between 1 and 30)
  `restaurant_id` (foreign key)
  `pizza_id` (foreign key)


   Setup Instructions

1. Clone the repo and enter the backend folder:
   ```bash
   git clone https://github.com/natasha-wairimu/pizza-api.git
   cd pizza-api/server
Create a virtual environment:
   pipenv install
   pipenv shell

Copy
flask db init  # only if running for the first time
flask db migrate -m "init"
flask db upgrade
Seed the database (if seed.py is available):

Copy
python seed.py
Start the server:

flask run --port=5555
API Endpoints
GET /restaurants
Returns a list of all restaurants.

GET /restaurants/<id>
Returns a single restaurant with its pizzas.
Returns 404 if not found.

DELETE /restaurants/<id>
Deletes the restaurant and its related data.

GET /pizzas
Returns all pizzas in the system.

POST /restaurant_pizzas
Adds a pizza to a restaurant with a custom price.

Body example:

json
Copy
{
  "price": 20,
  "pizza_id": 1,
  "restaurant_id": 2
}
On success (201):

json
Copy
{
  "id": 1,
  "name": "Hawaiian",
  "ingredients": "Cheese, Pineapple, Ham"
}
Notes
Only prices between 1 and 30 are allowed.

If you try to link a pizza or restaurant that doesn’t exist, it will return a helpful error.

I used Postman to test all routes and handle edge cases.

Author
Built by Natasha Wairimu
Phase 4 – Pizza Code Challenge
July 2025