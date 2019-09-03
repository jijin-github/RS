# RS
Reservation System

Sample API ENdpoints

Create User

http://localhost:5000/user/?email=admin_user@gmail.com&mobile=99999&password=1234&type=admin
http://localhost:5000/user/ (GET)

Create Country

http://localhost:5000/country?code=IN&name=India (POST)
http://localhost:5000/country/ (GET)

Create State

http://localhost:5000/state/?country_id=1&name=karnataka (POST)
http://localhost:5000/state/ (GET)


Create Place

http://localhost:5000/place/?state_id=1&name=bangalore (POST)
http://localhost:5000/place/ (GET)

Create Restaurant Categories

http://localhost:5000/restaurant-categories/?name=fast food (POST)
http://localhost:5000/estaurant-categories/ (GET)

Create Table Category

http://localhost:5000/table-categories?title=AC&price=500 (POST)
http://localhost:5000/table-categories (GET)

Create Restaurant

http://localhost:5000/restaurant?user_email=adminemail@gmail.com&restaurant_category_id=1&place_id=1&title=Zam Zam&description=Tasty&mobile=999999&email=zam@yahoo.com&opening_time=09:00&closing_time=21:00 (POST)
http://localhost:5000/restaurant (GET)

Create Table

http://localhost:5000/table/?table_category_id=1&restaurant_id=1&seat_count=10&count=3 (POST)
http://localhost:5000/table/ (GET)

Create Menu

http://localhost:5000/menu-items/?restaurant_id=1&name=Noodles&description=Test.....&price=130 (POST)
http://localhost:5000/menu-items/ (GET)

Create Order

http://localhost:5000/book?user_email=customer1@gmail.com&mobile=9999999&restaurant_id=1&spend_hour=3&table=1&selected_item={"item_id":1, "item_count":2} (POST)
http://localhost:5000/book/ (GET)
