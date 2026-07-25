from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory store for Hands-On 4 (replaced by SQLAlchemy in Hands-On 5)
_courses = []
_next_id = 1


def make_response_json(data, status_code=200):
    """Consistent JSON envelope helper (Task 2, step 44)."""
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(_courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    global _next_id
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

    required = ['name', 'code', 'credits']
    missing = [f for f in required if f not in payload]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing fields: {", ".join(missing)}'}), 400

    course = {'id': _next_id, **payload}
    _courses.append(course)
    _next_id += 1
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400
    course.update(payload)
    return make_response_json(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global _courses
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    _courses = [c for c in _courses if c['id'] != course_id]
    return make_response_json(None, 200)
