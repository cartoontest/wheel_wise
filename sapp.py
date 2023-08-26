from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

wheel_balancing_spaces = [{'id': 1, 'status': 'free'}, {'id': 2, 'status': 'free'}, {'id': 3, 'status': 'free'}]

# loading data at the beginning
try:
    with open('wheel_balancing_spaces.json', 'r') as f:
        wheel_balancing_spaces = json.load(f)
except FileNotFoundError:
    pass

# sending inform about wheel_balancing
@app.route('/wheel_balancing_info', methods=['GET'])
def get_wheel_balancing_info():
    free_spaces = sum(1 for space in wheel_balancing_spaces if space['status'] == 'free')
    wheel_balancing_info = {
        'free_spaces': free_spaces,
        'total_spaces': len(wheel_balancing_spaces)
    }
    return jsonify(wheel_balancing_info)

@app.route('/wheel_balancing/free_spaces', methods=['GET'])
def get_free_spaces():
    free_spaces = [{'id': space['id'], 'status': space['status']} for space in wheel_balancing_spaces if space['status'] == 'free']
    return jsonify(free_spaces)

@app.route('/wheel_balancing/free_spaces_with_id', methods=['GET'])
def get_free_spaces_with_id():
    free_spaces = [{'id': space['id'], 'status': space['status']} for space in wheel_balancing_spaces if space['status'] == 'free']
    return jsonify(free_spaces)

# reserve wheel_balancing
@app.route('/wheel_balancing/reserve', methods=['POST'])
def reserve_wheel_balancing_space():
    data = request.get_json()
    space_id = data.get('id')
    name = data.get('name')
    phone = data.get('phone')
    
    print(f"Received data: {data}")

    if space_id is None:
        return 'Space id is missing', 400

    space = next((space for space in wheel_balancing_spaces if space['id'] == space_id), None)

    if space is None:
        return 'Space not found', 404

    if space['status'] != 'free':
        return 'Space is already occupied', 409

    space['status'] = 'reserved'
    space['name'] = name
    space['phone'] = phone

    print(f"Successfully reserved wheel_balancing space {space_id} for {name} ({phone})")

    # Save the updated wheel_balancing spaces data to file
    with open('wheel_balancing_spaces.json', 'w') as f:
        json.dump(wheel_balancing_spaces, f)

    return f"Successfully reserved wheel_balancing space {space_id} for {name} ({phone})"

    return 'Space reserved successfully', 200

# sending info about reserving wheel_balancing place
@app.route('/wheel_balancing/cancel', methods=['POST'])
def cancel_wheel_balancing_reservation():
    data = request.get_json()
    space_id = data.get('id')

    if space_id is None:
        return 'Space id is missing', 400

    space = next((space for space in wheel_balancing_spaces if space['id'] == space_id), None)

    if space is None:
        return 'Space not found', 404

    if space['status'] != 'reserved':
        return 'Space is not reserved', 409

    space['status'] = 'free'
    space.pop('name', None)
    space.pop('phone', None)

    # Save the updated wheel_balancing spaces data to file
    with open('wheel_balancingg_spaces.json', 'w') as f:
        json.dump(wheel_balancing_spaces, f)

    return 'Reservation canceled successfully', 200

if __name__ == '__main__':
    app.run(port=8000)