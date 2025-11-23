from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Path to the data file
DATA_FILE = 'data/fruits.json'

def load_fruits():
    """Load fruits from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"fruits": [], "categories": []}

def save_fruits(data):
    """Save fruits to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_id(fruits):
    """Get the next available ID for a new fruit"""
    if not fruits:
        return 1
    return max(fruit['id'] for fruit in fruits) + 1

# Routes

@app.route('/')
def home():
    """API information endpoint"""
    return jsonify({
        "name": "Fruit Store API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /fruits": "Get all fruits",
            "GET /fruits/<id>": "Get a specific fruit",
            "POST /fruits": "Create a new fruit",
            "PUT /fruits/<id>": "Update a fruit",
            "DELETE /fruits/<id>": "Delete a fruit",
            "GET /categories": "Get all categories",
            "POST /categories": "Create a new category",
            "DELETE /categories/<name>": "Delete a category",
            "GET /fruits/category/<category>": "Get fruits by category"
        }
    })

@app.route('/fruits', methods=['GET'])
def get_fruits():
    """Get all fruits or filter by query parameters"""
    data = load_fruits()
    fruits = data.get('fruits', [])

    # Filter by search query if provided
    search = request.args.get('search', '').lower()
    if search:
        fruits = [f for f in fruits if search in f['name'].lower()]

    # Filter by category if provided
    category = request.args.get('category', '').lower()
    if category:
        fruits = [f for f in fruits if f.get('category', '').lower() == category]

    return jsonify({
        "total": len(fruits),
        "fruits": fruits
    })

@app.route('/fruits/<int:fruit_id>', methods=['GET'])
def get_fruit(fruit_id):
    """Get a specific fruit by ID"""
    data = load_fruits()
    fruits = data.get('fruits', [])

    fruit = next((f for f in fruits if f['id'] == fruit_id), None)

    if fruit:
        return jsonify(fruit)
    return jsonify({"error": "Fruit not found"}), 404

@app.route('/fruits', methods=['POST'])
def create_fruit():
    """Create a new fruit"""
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Name is required"}), 400

    data = load_fruits()
    fruits = data.get('fruits', [])
    categories = data.get('categories', [])

    # Validate category if provided
    category = request.json.get('category', '')
    if category and category not in categories:
        return jsonify({"error": f"Category '{category}' does not exist"}), 400

    new_fruit = {
        'id': get_next_id(fruits),
        'name': request.json['name'],
        'category': category,
        'color': request.json.get('color', ''),
        'price': request.json.get('price', 0),
        'quantity': request.json.get('quantity', 0),
        'description': request.json.get('description', ''),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    fruits.append(new_fruit)
    data['fruits'] = fruits
    save_fruits(data)

    return jsonify(new_fruit), 201

@app.route('/fruits/<int:fruit_id>', methods=['PUT'])
def update_fruit(fruit_id):
    """Update an existing fruit"""
    data = load_fruits()
    fruits = data.get('fruits', [])
    categories = data.get('categories', [])

    fruit_index = next((i for i, f in enumerate(fruits) if f['id'] == fruit_id), None)

    if fruit_index is None:
        return jsonify({"error": "Fruit not found"}), 404

    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    # Validate category if provided
    category = request.json.get('category', fruits[fruit_index].get('category', ''))
    if category and category not in categories:
        return jsonify({"error": f"Category '{category}' does not exist"}), 400

    # Update fruit fields
    fruits[fruit_index]['name'] = request.json.get('name', fruits[fruit_index]['name'])
    fruits[fruit_index]['category'] = category
    fruits[fruit_index]['color'] = request.json.get('color', fruits[fruit_index].get('color', ''))
    fruits[fruit_index]['price'] = request.json.get('price', fruits[fruit_index].get('price', 0))
    fruits[fruit_index]['quantity'] = request.json.get('quantity', fruits[fruit_index].get('quantity', 0))
    fruits[fruit_index]['description'] = request.json.get('description', fruits[fruit_index].get('description', ''))
    fruits[fruit_index]['updated_at'] = datetime.now().isoformat()

    data['fruits'] = fruits
    save_fruits(data)

    return jsonify(fruits[fruit_index])

@app.route('/fruits/<int:fruit_id>', methods=['DELETE'])
def delete_fruit(fruit_id):
    """Delete a fruit"""
    data = load_fruits()
    fruits = data.get('fruits', [])

    fruit_index = next((i for i, f in enumerate(fruits) if f['id'] == fruit_id), None)

    if fruit_index is None:
        return jsonify({"error": "Fruit not found"}), 404

    deleted_fruit = fruits.pop(fruit_index)
    data['fruits'] = fruits
    save_fruits(data)

    return jsonify({"message": "Fruit deleted successfully", "fruit": deleted_fruit})

# Category endpoints

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    data = load_fruits()
    categories = data.get('categories', [])

    # Get fruit count for each category
    fruits = data.get('fruits', [])
    category_counts = {}
    for fruit in fruits:
        cat = fruit.get('category', '')
        if cat:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    result = [
        {"name": cat, "fruit_count": category_counts.get(cat, 0)}
        for cat in categories
    ]

    return jsonify({
        "total": len(categories),
        "categories": result
    })

@app.route('/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Category name is required"}), 400

    data = load_fruits()
    categories = data.get('categories', [])

    new_category = request.json['name']

    if new_category in categories:
        return jsonify({"error": "Category already exists"}), 400

    categories.append(new_category)
    data['categories'] = categories
    save_fruits(data)

    return jsonify({"message": "Category created successfully", "category": new_category}), 201

@app.route('/categories/<string:category_name>', methods=['DELETE'])
def delete_category(category_name):
    """Delete a category"""
    data = load_fruits()
    categories = data.get('categories', [])

    if category_name not in categories:
        return jsonify({"error": "Category not found"}), 404

    # Check if any fruits use this category
    fruits = data.get('fruits', [])
    fruits_in_category = [f for f in fruits if f.get('category', '') == category_name]

    if fruits_in_category:
        return jsonify({
            "error": f"Cannot delete category. {len(fruits_in_category)} fruit(s) are using this category"
        }), 400

    categories.remove(category_name)
    data['categories'] = categories
    save_fruits(data)

    return jsonify({"message": "Category deleted successfully", "category": category_name})

@app.route('/fruits/category/<string:category>', methods=['GET'])
def get_fruits_by_category(category):
    """Get all fruits in a specific category"""
    data = load_fruits()
    fruits = data.get('fruits', [])
    categories = data.get('categories', [])

    if category not in categories:
        return jsonify({"error": "Category not found"}), 404

    category_fruits = [f for f in fruits if f.get('category', '') == category]

    return jsonify({
        "category": category,
        "total": len(category_fruits),
        "fruits": category_fruits
    })

if __name__ == '__main__':
    # Create initial data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        initial_data = {
            "fruits": [],
            "categories": ["Citrus", "Berries", "Tropical", "Stone Fruits", "Pome Fruits", "Melons"]
        }
        save_fruits(initial_data)
        print(f"Created initial data file at {DATA_FILE}")

    print("Starting Fruit Store API...")
    print("Access the API at http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)