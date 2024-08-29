import json
import uuid
from typing import Dict, List
from flask import Flask, jsonify, request

app = Flask(__name__)

employees: List[Dict[str, str]] = [
    {'id': str(uuid.uuid4()), 'name': 'Gebre'},
    {'id': str(uuid.uuid4()), 'name': 'Alen'},
    {'id': str(uuid.uuid4()), 'name': 'Malin'}
]


@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Employee API!'


@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)


@app.route('/employees/<id>', methods=['GET'])
def get_employee_by_id(id: str):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)


def get_employee(id: str):
    return next((e for e in employees if e['id'] == id), None)


def employee_is_valid(employee: Dict[str, str]) -> bool:
    return 'name' in employee and len(employee) == 1


@app.route('/employees', methods=['POST'])
def create_employee():
    try:
        employee = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data.'}), 400

    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    employee['id'] = str(uuid.uuid4())
    employees.append(employee)

    return '', 201, {'location': f'/employees/{employee["id"]}'}


@app.route('/employees/<id>', methods=['PUT'])
def update_employee(id: str):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    try:
        updated_employee = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data.'}), 400

    if not employee_is_valid(updated_employee):
        return jsonify({'error': 'Invalid employee properties.'}), 400

    employee.update(updated_employee)

    return jsonify(employee)


@app.route('/employees/<id>', methods=['DELETE'])
def delete_employee(id: str):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404

    employees[:] = [e for e in employees if e['id'] != id]
    return jsonify(employee), 200


if __name__ == '__main__':
    app.run(port=5000)
