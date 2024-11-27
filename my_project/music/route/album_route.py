from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response

from my_project.music.controller import album_controller
from my_project.music.domain import Album

album_bp = Blueprint('albums', __name__, url_prefix='/albums')


@album_bp.get('')
def get_all_albums() -> Response:
    return make_response(jsonify(album_controller.find_all()), HTTPStatus.OK)


@album_bp.get("/latest")
def get_latest_album() -> Response:
    return make_response(jsonify(Album.put_into_dto(album_controller.get_latest_created_album())), HTTPStatus.OK)


@album_bp.post('')
def create_album() -> Response:
    content = request.get_json()
    album = Album.create_from_dto(content)
    created_album = album_controller.create(album)
    return make_response(jsonify(created_album), HTTPStatus.CREATED)


@album_bp.post('/reserve-copy')
def reserve_copy() -> Response:
    album_controller.reserve_copy()

    return make_response(jsonify({"message": "Success"}), HTTPStatus.CREATED)


@album_bp.post("/<string:album_name>/add_compositor/<string:compositor_name>")
def add_compositor(album_name: str, compositor_name: str) -> Response:
    album_controller.add_compositor(album_name, compositor_name)

    return make_response(jsonify({"message": "Success"}), HTTPStatus.CREATED)


@album_bp.get('/<int:album_id>')
def get_album(album_id: int) -> Response:
    return make_response(jsonify(album_controller.find_by_id(album_id)), HTTPStatus.OK)


@album_bp.put('/<int:album_id>')
def update_album(album_id: int) -> Response:
    content = request.get_json()
    album = Album.create_from_dto(content)
    album_controller.update(album_id, album)
    return make_response("Album updated", HTTPStatus.OK)


@album_bp.patch('/<int:album_id>')
def patch_album(album_id: int) -> Response:
    content = request.get_json()
    album_controller.patch(album_id, content)
    return make_response("Album updated", HTTPStatus.OK)


@album_bp.delete('/<int:album_id>')
def delete_album(album_id: int) -> Response:
    album_controller.delete(album_id)
    return make_response("Album deleted", HTTPStatus.OK)


@album_bp.get('/search')
def find_album_by_name() -> Response:
    name = request.args.get("name")
    if not name:
        return make_response(jsonify({"error": "Name parameter is required"}), HTTPStatus.BAD_REQUEST)

    album = album_controller.get_album_by_name(name)
    if album:
        return make_response(jsonify(album), HTTPStatus.OK)

    return make_response(jsonify({"error": "Album not found"}), HTTPStatus.NOT_FOUND)
