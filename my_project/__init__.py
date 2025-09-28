import os
from http import HTTPStatus
import secrets
from typing import Dict, Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from my_project.label.route import register_routes as register_label_routes
from my_project.music.route import register_routes as register_music_routes

import pymysql
pymysql.install_as_MySQLdb()

SECRET_KEY = "SECRET_KEY"
SQLALCHEMY_DATABASE_URI = "SQLALCHEMY_DATABASE_URI"
MYSQL_ROOT_USER = "MYSQL_ROOT_USER"
MYSQL_ROOT_PASSWORD = "MYSQL_ROOT_PASSWORD"

# Database
db = SQLAlchemy()

todos = {}


def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    """
    Creates Flask application
    :param app_config: Flask configuration
    :param additional_config: additional configuration
    :return: Flask application object
    """
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv(SECRET_KEY) or secrets.token_hex(16)
    app.config.update(app_config)

    _init_db(app)
    register_label_routes(app)
    register_music_routes(app)
    _init_swagger(app)

    return app


def _init_swagger(app: Flask) -> None:
    """
    Serve Swagger UI and OpenAPI spec for this backend.
    """
    from flask import send_from_directory

    swagger_dir = os.path.join(os.path.dirname(__file__), "swagger")
    spec_filename = "openapi.json"

    @app.route("/swagger.json")
    def swagger_json():
        return send_from_directory(swagger_dir, spec_filename, mimetype="application/json")

    @app.route("/docs")
    def swagger_ui():
        return (
            """
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>API Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
window.onload = () => {
  window.ui = SwaggerUIBundle({
    url: '/swagger.json',
    dom_id: '#swagger-ui'
  });
};
</script>
</body>
</html>
""",
            HTTPStatus.OK,
            {"Content-Type": "text/html; charset=utf-8"},
        )


def _init_db(app: Flask) -> None:
    """
    Initializes DB with SQLAlchemy
    :param app: Flask application object
    """
    db.init_app(app)

    if not database_exists(app.config[SQLALCHEMY_DATABASE_URI]):
        create_database(app.config[SQLALCHEMY_DATABASE_URI])

    import my_project.label.domain
    import my_project.music.domain

    with app.app_context():
        db.create_all()


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    """
    Processes input configuration. Secrets must come from environment variables (.env), not YAML.
    :param app_config: Flask configuration (may already include SQLALCHEMY_DATABASE_URI)
    :param additional_config: deprecated, not used for secrets
    """
    # If a full SQLALCHEMY_DATABASE_URI is provided, keep it.
    uri = app_config.get(SQLALCHEMY_DATABASE_URI) or os.getenv(SQLALCHEMY_DATABASE_URI)

    # Otherwise, try to construct from individual env vars
    if not uri:
        user = os.getenv("DB_USER") or os.getenv(MYSQL_ROOT_USER)
        password = os.getenv("DB_PASSWORD") or os.getenv(MYSQL_ROOT_PASSWORD)
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT")
        name = os.getenv("DB_NAME")
        if user and password and name:
            hostport = f"{host}:{port}" if port else host
            dialect = os.getenv("DB_DIALECT", "mysql")
            uri = f"{dialect}://{user}:{password}@{hostport}/{name}"

    # As a final fallback (mostly for local dev), use sqlite file if not set
    if not uri:
        uri = "sqlite:///device_db.sqlite"

    app_config[SQLALCHEMY_DATABASE_URI] = uri
    # No return needed
