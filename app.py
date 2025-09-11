
import json
import logging
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

CARS_FILE = 'cars.json'
BATTERY_FILE = 'battery.json'

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

def read_json_file(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            logger.debug("Loaded %s", filepath)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.warning("Could not read %s: %s", filepath, exc)
        return []

def write_json_file(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    logger.debug("Wrote %s", filepath)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = read_json_file(CARS_FILE)
    return jsonify(cars)

@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json()
    if not data or 'name' not in data or 'capacity' not in data:
        logger.error("Invalid car data: %s", data)
        return jsonify({'error': 'Invalid data'}), 400
    
    cars = read_json_file(CARS_FILE)
    cars.append(data)
    write_json_file(CARS_FILE, cars)
    return jsonify(data), 201

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'capacity' not in data or 'current_charge' not in data:
        logger.error("Invalid calculation data: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    try:
        capacity = float(data['capacity'])
        current_charge = float(data['current_charge'])
    except ValueError:
        logger.error("Invalid number format in data: %s", data)
        return jsonify({'error': 'Invalid number format'}), 400

    if not (0 <= current_charge <= 100):
        logger.error("Current charge out of range: %s", current_charge)
        return jsonify({'error': 'Current charge must be between 0 and 100'}), 400

    charge_to_80_percent = max(0, 80 - current_charge)
    kwh_needed = (charge_to_80_percent / 100) * capacity
    
    result = {'kwh_needed': round(kwh_needed, 2)}
    write_json_file(BATTERY_FILE, result)
    logger.info(
        "Calculated kWh needed: %s for capacity=%s current_charge=%s",
        result['kwh_needed'],
        capacity,
        current_charge,
    )

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
