from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response

from my_project.music.domain import Genre

from my_project.music.controller import genre_controller

genre_bp = Blueprint('genres', __name__, url_prefix='/genres')


@genre_bp.get('')
def get_genres():
    return make_response(jsonify(genre_controller.find_all()), HTTPStatus.OK)


@genre_bp.get('/<int:genre_id>')
def get_genre(genre_id):
    return make_response(jsonify(genre_controller.find_by_id(genre_id)), HTTPStatus.OK)


@genre_bp.post('')
def create_genre() -> Response:
    content = request.get_json()
    compositor = Genre.create_from_dto(content)
    created_compositor = genre_controller.create(compositor)
    return make_response(jsonify(created_compositor), HTTPStatus.CREATED)


@genre_bp.post('/create-noname')
def create_noname() -> Response:
    genre_controller.create_noname_genres()

    return make_response("Genre created", HTTPStatus.CREATED)


@genre_bp.put('/<int:genre_id>')
def update_compositor(genre_id: int) -> Response:
    content = request.get_json()
    genre = Genre.create_from_dto(content)
    genre_controller.update(genre_id, genre)
    return make_response("Genre updated", HTTPStatus.OK)


@genre_bp.patch('/<int:genre_id>')
def patch_compositor(genre_id: int) -> Response:
    content = request.get_json()
    genre_controller.patch(genre_id, content)
    return make_response("Genre updated", HTTPStatus.OK)


@genre_bp.delete('/<int:compositor_id>')
def delete_compositor(compositor_id: int) -> Response:
    genre_controller.delete(compositor_id)
    return make_response("Genre deleted", HTTPStatus.OK)
