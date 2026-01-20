from flask import Flask, request, jsonify

app = Flask(__name__)

items = [
    {'id': 1, 'name': 'mayur', 'subject':'math', 'marks':85},
    {'id': 2, 'name': 'sagar', 'subject':'science', 'marks':95},
    {'id': 3, 'name': 'sia', 'subject':'psychology', 'marks':87}    
]
next_id=3
@app.route('/')
def home():
    return "Welcome to the Flask CRUD API"

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'message':'Identity not found'}),404

@app.route('/',methods=['POST'])
def create_item():
    global next_id
    new_item_data = request.get_json()

    if not new_item_data or 'name' not in new_item_data or 'subject' not in new_item_data or 'marks' not in new_item_data:
        return jsonify({'message': 'Invalid data provided'}), 400

    new_item ={
        'id': next_id,
        'name': new_item_data['name'],
        'subject':new_item_data['subject'],
        'marks':new_item_data['marks']
    }
    items.append(new_item)
    next_id+=1
    return jsonify(new_item),201

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        update_data=request.get_json()
        if 'name' in update_data:
            item['name']= update_data['name']
        if 'subject' in update_data:
            item['subject']= update_data['subject']
        if 'marks' in update_data:
            item['marks']=update_data['marks']
        return jsonify(item)
    return jsonify({'message': 'Identity not Found'}),404

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        items = [i for i in items if i['id'] != item_id]
        return jsonify({'message': f'Item {item_id} deleted'})
    return jsonify({'message': 'Item not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)