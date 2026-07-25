"""Course Service - owns Department & Course data. Runs on port 5001."""
from flask import Flask, jsonify, request

app = Flask(__name__)

_courses = {
    1: {'id': 1, 'name': 'Data Structures', 'code': 'CS101', 'credits': 4},
    2: {'id': 2, 'name': 'Operating Systems', 'code': 'CS102', 'credits': 4},
}


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    return jsonify(list(_courses.values()))


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = _courses.get(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course)


@app.route('/api/courses/', methods=['POST'])
def create_course():
    payload = request.get_json() or {}
    new_id = max(_courses.keys(), default=0) + 1
    course = {'id': new_id, **payload}
    _courses[new_id] = course
    return jsonify(course), 201


if __name__ == '__main__':
    app.run(port=5001, debug=True)
