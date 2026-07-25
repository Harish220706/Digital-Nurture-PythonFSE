"""
Student Service - owns Student & Enrollment data. Runs on port 5002.
Calls Course Service (via HTTP) to verify a course exists before enrolling
a student - this is synchronous inter-service communication.
"""
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

COURSE_SERVICE_URL = 'http://localhost:5001'

_students = {
    1: {'id': 1, 'first_name': 'Asha', 'last_name': 'Rao', 'email': 'asha@college.edu'},
}
_enrollments = []


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify(list(_students.values()))


@app.route('/api/students/', methods=['POST'])
def create_student():
    payload = request.get_json() or {}
    new_id = max(_students.keys(), default=0) + 1
    student = {'id': new_id, **payload}
    _students[new_id] = student
    return jsonify(student), 201


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll(student_id):
    if student_id not in _students:
        return jsonify({'error': 'Student not found'}), 404

    payload = request.get_json() or {}
    course_id = payload.get('course_id')

    # Inter-service call: verify the course exists via Course Service's own API.
    try:
        resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=3)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Course Service unavailable'}), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 404

    enrollment = {'student_id': student_id, 'course_id': course_id, 'course': resp.json()}
    _enrollments.append(enrollment)
    return jsonify(enrollment), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
