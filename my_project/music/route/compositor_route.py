from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response

from my_project.music.domain import Compositor

from my_project.music.controller import compositor_controller

compositor_bp = Blueprint('compositors', __name__, url_prefix='/compositors')


@compositor_bp.get('')
def get_all_compositors() -> Response:
    """
    Gets all Compositor objects from the table using the Service layer.
    :return: Response object with a list of Compositors as DTOs
    """
    return make_response(jsonify(compositor_controller.find_all()), HTTPStatus.OK)


@compositor_bp.post('')
def create_compositor() -> Response:
    """
    Creates a new Compositor object using the Service layer.
    :return: Response object with created Compositor as a DTO
    """
    content = request.get_json()
    compositor = Compositor.create_from_dto(content)
    created_compositor = compositor_controller.create(compositor)
    return make_response(jsonify(created_compositor), HTTPStatus.CREATED)


@compositor_bp.get('/<int:compositor_id>')
def get_compositor(compositor_id: int) -> Response:
    """
    Gets a Compositor by ID.
    :param compositor_id: ID of the Compositor
    :return: Response object with the Compositor as a DTO
    """
    return make_response(jsonify(compositor_controller.find_by_id(compositor_id)), HTTPStatus.OK)


@compositor_bp.put('/<int:compositor_id>')
def update_compositor(compositor_id: int) -> Response:
    """
    Updates a Compositor by ID.
    :param compositor_id: ID of the Compositor
    :return: Response object confirming update
    """
    content = request.get_json()
    compositor = Compositor.create_from_dto(content)
    compositor_controller.update(compositor_id, compositor)
    return make_response("Compositor updated", HTTPStatus.OK)


@compositor_bp.patch('/<int:compositor_id>')
def patch_compositor(compositor_id: int) -> Response:
    """
    Patches a Compositor by ID.
    :param compositor_id: ID of the Compositor
    :return: Response object confirming patch
    """
    content = request.get_json()
    compositor_controller.patch(compositor_id, content)
    return make_response("Compositor updated", HTTPStatus.OK)


@compositor_bp.delete('/<int:compositor_id>')
def delete_compositor(compositor_id: int) -> Response:
    """
    Deletes a Compositor by ID.
    :param compositor_id: ID of the Compositor
    :return: Response object confirming deletion
    """
    compositor_controller.delete(compositor_id)
    return make_response("Compositor deleted", HTTPStatus.OK)


@compositor_bp.get('/search')
def find_compositor_by_name() -> Response:
    """
    Searches for a Compositor by name.
    :return: Response object with the found Compositor as a DTO, or 404 if not found
    """
    name = request.args.get("name")
    if not name:
        return make_response(jsonify({"error": "Name parameter is required"}), HTTPStatus.BAD_REQUEST)

    compositor = compositor_controller.get_compositor_by_name(name)
    if compositor:
        return make_response(jsonify(compositor), HTTPStatus.OK)

    return make_response(jsonify({"error": "Compositor not found"}), HTTPStatus.NOT_FOUND)


@compositor_bp.route('/<int:compositor_id>/albums', methods=['POST'])
def add_album_to_compositor(compositor_id: int):
    data = request.get_json()
    album_id = data.get("album_id")

    if not album_id:
        return make_response(jsonify({"error": "album_id is required"}), HTTPStatus.BAD_REQUEST)

    result = compositor_controller.add_album(compositor_id, album_id)
    if "error" in result:
        return make_response(jsonify(result), HTTPStatus.NOT_FOUND)

    return make_response(jsonify(result), HTTPStatus.CREATED)
