from typing import Optional, Dict, Any

from .general_controller import GeneralController
from my_project.music.service import compositor_service


class CompositorController(GeneralController):
    """
    Realisation of Compositor controller.
    """
    _service = compositor_service

    def get_compositor_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Gets a Compositor object by name from the database using the Service layer as a DTO object.
        :param name: The name of the Compositor
        :return: A dictionary representing the Compositor as a DTO or None if not found
        """
        compositor = self._service.find_compositor_by_name(name)
        return compositor.put_into_dto() if compositor else None

    def add_album(self, compositor_id: int, album_id: int):
        try:
            self._service.add_album_to_compositor(compositor_id, album_id)
            return {"message": "Album added to compositor"}
        except ValueError as e:
            return {"error": str(e)}
