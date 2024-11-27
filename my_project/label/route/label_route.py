from http import HTTPStatus

from flask import Blueprint, jsonify, Response, request, make_response

from my_project.label.controller import label_controller
from my_project.label.domain import Label

label_bp = Blueprint('labels', __name__, url_prefix='/labels')


@label_bp.get('')
def get_all_client_types() -> Response:
    """
    Gets all objects from table using Service layer.
    :return: Response object
    """
    return make_response(jsonify(label_controller.find_all()), HTTPStatus.OK)


@label_bp.post('')
def create_client_type() -> Response:
    """
    Gets all objects from table using Service layer.
    :return: Response object
    """
    content = request.get_json()
    label = Label.create_from_dto(content)
    label_controller.create(label)
    return make_response(jsonify(label.put_into_dto()), HTTPStatus.CREATED)


@label_bp.get('/<int:label_id>')
def get_client_type(label_id: int) -> Response:
    """
    Gets client_type by ID.
    :return: Response object
    """
    return make_response(jsonify(label_controller.find_by_id(label_id)), HTTPStatus.OK)


@label_bp.put('/<int:label_id>')
def update_client_type(label_id: int) -> Response:
    """
    Updates label by ID.
    :return: Response object
    """
    content = request.get_json()
    label = Label.create_from_dto(content)
    label_controller.update(label_id, label)
    return make_response("Label updated", HTTPStatus.OK)


@label_bp.patch('/<int:label_id>')
def patch_client_type(label_id: int) -> Response:
    """
    Patches label by ID.
    :return: Response object
    """
    content = request.get_json()
    label_controller.patch(label_id, content)
    return make_response("Client updated", HTTPStatus.OK)


@label_bp.delete('/<int:label_id>')
def delete_client_type(label_id: int) -> Response:
    """
    Deletes label by ID.
    :return: Response object
    """
    label_controller.delete(label_id)
    return make_response("Client deleted", HTTPStatus.OK)
