from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from courses.routes import courses_bp
    app.register_blueprint(courses_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

    @app.route('/')
    def index():
        return jsonify({'message': 'Course Management API (Flask + SQLAlchemy) is running'})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
