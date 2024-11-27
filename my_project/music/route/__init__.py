from flask import Flask
from .error_handler import err_handler_bp


def register_routes(app: Flask) -> None:
    """
    Registers all necessary Blueprint routes
    :param app: Flask application object
    """
    app.register_blueprint(err_handler_bp)

    from .compositor_route import compositor_bp
    from .album_route import album_bp
    from .genre_route import genre_bp

    app.register_blueprint(compositor_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(genre_bp)
