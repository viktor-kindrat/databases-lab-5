import os

from waitress import serve
from dotenv import load_dotenv

from my_project import create_app

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"

if __name__ == '__main__':
    load_dotenv()

    flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

    common_config = {
        "DEBUG": os.getenv("DEBUG", "False").lower() in ("1", "true", "yes"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    sqlalchemy_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not sqlalchemy_uri and flask_env == DEVELOPMENT:
        sqlalchemy_uri = "sqlite:///device_db.sqlite"
    if sqlalchemy_uri:
        common_config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_uri

    if flask_env == DEVELOPMENT:
        create_app(common_config, {}).run(port=DEVELOPMENT_PORT, debug=True)

    elif flask_env == PRODUCTION:
        serve(create_app(common_config, {}), host=HOST, port=int(os.getenv("APP_PORT", PRODUCTION_PORT)))

    else:
        raise ValueError(f"Check OS environment variable '{FLASK_ENV}'")
