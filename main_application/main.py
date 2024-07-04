import random
import os
import uuid
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://root:example@mongo:27017/")
db = client['dinner_suggestions']
collection = db['suggestions']

main_dishes = [
    "Spaghetti Carbonara", "Grilled Chicken Caesar Salad", "Vegetable Stir-Fry", "Beef Tacos",
    "Mushroom Risotto", "Teriyaki Salmon", "Pasta Primavera", "BBQ Ribs", "Chicken Alfredo",
    "Shrimp Scampi", "Lamb Chops", "Veggie Burger"
]

side_dishes = [
    "Garlic Bread", "Steamed Broccoli", "Roasted Potatoes", "Caprese Salad",
    "Quinoa Pilaf", "Grilled Asparagus", "Caesar Salad", "French Fries",
    "Mashed Potatoes", "Brussels Sprouts", "Corn on the Cob", "Coleslaw"
]

desserts = [
    "Chocolate Lava Cake", "Fruit Salad", "Cheesecake", "Apple Pie",
    "Tiramisu", "Ice Cream Sundae", "Brownies", "Lemon Tart",
    "Panna Cotta", "Macarons", "Cupcakes", "Strawberry Shortcake"
]

def get_complex_dinner_suggestion():
    main_dish = random.choice(main_dishes)
    side_dish = random.choice(side_dishes)
    dessert = random.choice(desserts)
    suggestion = {
        'main': main_dish,
        'side': side_dish,
        'dessert': dessert,
        'timestamp': datetime.utcnow()
    }
    collection.insert_one(suggestion)
    return main_dish, side_dish, dessert

@app.route('/')
def index():
    main, side, dessert = get_complex_dinner_suggestion()
    dish_count = collection.count_documents({})
    
    pod_info = {
        'uuid': str(uuid.uuid4()),
        'hostname': os.uname().nodename,
        'datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return render_template('index.html', main=main, side=side, dessert=dessert,dish_count=dish_count, info=pod_info)

@app.route('/refresh')
def refresh():
    main, side, dessert = get_complex_dinner_suggestion()
    return jsonify(main=main, side=side, dessert=dessert)

@app.route('/last5')
def last5():
    last_five = list(collection.find().sort('timestamp', -1).limit(5))
    for item in last_five:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return jsonify(last_five)

@app.route('/all_suggestions')
def all_suggestions():
    all_suggestions = list(collection.find().sort('timestamp', -1))
    for item in all_suggestions:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return jsonify(all_suggestions)

@app.route('/week_suggestions')
def week_suggestions():
    suggestions = []
    for _ in range(7):
        main, side, dessert = get_complex_dinner_suggestion()
        suggestions.append({'main': main, 'side': side, 'dessert': dessert})
    return jsonify(suggestions)

@app.route('/last30')
def last30():
    last_thirty = list(collection.find().sort('timestamp', -1).limit(30))
    for item in last_thirty:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string
    return jsonify(last_thirty)

@app.route('/dish_count')
def get_dish_count():
    dish_count = collection.count_documents({})
    return jsonify({'count': dish_count})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")