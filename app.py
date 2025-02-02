from flask import Flask, jsonify, request
from flask_cors import CORS
from mongo import init_db
import uuid

app = Flask(__name__)
CORS(app)
mongo = init_db(app)

# Product Endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(mongo.db.products.find())
    return jsonify([{**p, '_id': str(p['_id'])} for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    if not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    product = {
        '_id': str(uuid.uuid4()),
        'name': data['name'],
        'price': float(data['price']),
        'image': data.get('image', '')
    }
    mongo.db.products.insert_one(product)
    return jsonify(product), 201

@app.route('/api/products/<id>', methods=['DELETE'])
def delete_product(id):
    result = mongo.db.products.delete_one({'_id': id})
    if result.deleted_count == 0:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': 'Product deleted'})

# Cart Endpoints
@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('productId')
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    mongo.db.cart.update_one(
        {'_id': 'main_cart'},
        {'$addToSet': {'items': product_id}},
        upsert=True
    )
    return jsonify({'message': 'Product added to cart'})

@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = mongo.db.cart.find_one({'_id': 'main_cart'})
    return jsonify({
        'items': cart.get('items', []) if cart else []
    })

@app.route('/api/cart/<product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    mongo.db.cart.update_one(
        {'_id': 'main_cart'},
        {'$pull': {'items': product_id}}
    )
    return jsonify({'message': 'Product removed from cart'})

if __name__ == '__main__':
    app.run(debug=True)