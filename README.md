# Fruit Store API

A simple RESTful API for managing a fruit store inventory, built with Flask.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete fruits
- **Categories**: Organize fruits by categories (Citrus, Berries, Tropical, etc.)
- **Search & Filter**: Search fruits by name or filter by category
- **Persistent Storage**: Data stored in JSON file
- **CORS Support**: Ready for frontend integration

## Installation

1. Ensure Python 3.x is installed on your system

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### General
- `GET /` - API information and available endpoints

### Fruits
- `GET /fruits` - Get all fruits (supports `?search=` and `?category=` filters)
- `GET /fruits/<id>` - Get a specific fruit
- `POST /fruits` - Create a new fruit
- `PUT /fruits/<id>` - Update a fruit
- `DELETE /fruits/<id>` - Delete a fruit

### Categories
- `GET /categories` - Get all categories with fruit counts
- `POST /categories` - Create a new category
- `DELETE /categories/<name>` - Delete a category
- `GET /fruits/category/<category>` - Get fruits by category

## Example Requests

### Get all fruits
```bash
curl http://localhost:5000/fruits
```

### Create a new fruit
```bash
curl -X POST http://localhost:5000/fruits \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Grape",
    "category": "Berries",
    "color": "Purple",
    "price": 2.99,
    "quantity": 50,
    "description": "Sweet purple grapes"
  }'
```

### Update a fruit
```bash
curl -X PUT http://localhost:5000/fruits/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1.29,
    "quantity": 45
  }'
```

### Delete a fruit
```bash
curl -X DELETE http://localhost:5000/fruits/1
```

### Search fruits
```bash
curl "http://localhost:5000/fruits?search=apple"
```

### Filter by category
```bash
curl "http://localhost:5000/fruits?category=Citrus"
```

## Data Structure

### Fruit Object
```json
{
  "id": 1,
  "name": "Orange",
  "category": "Citrus",
  "color": "Orange",
  "price": 0.99,
  "quantity": 50,
  "description": "Sweet and juicy orange",
  "created_at": "2025-11-23T00:00:00",
  "updated_at": "2025-11-23T00:00:00"
}
```

### Category
Categories are simple string values:
- Citrus
- Berries
- Tropical
- Stone Fruits
- Pome Fruits
- Melons

## File Structure

```
fruit-store-api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── data/
│   └── fruits.json    # Data storage file
├── tests/             # Test directory (for future tests)
└── venv/              # Virtual environment (not tracked in git)
```

## Development

The API runs in debug mode by default. To run in production, modify the last line in `app.py`:

```python
app.run(debug=False, host='0.0.0.0', port=5000)
```