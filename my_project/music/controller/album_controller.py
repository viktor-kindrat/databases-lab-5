from typing import Optional, Dict, Any
from my_project.music.service import album_service
from my_project.label.controller.general_controller import GeneralController


class AlbumController(GeneralController):
    _service = album_service

    def get_album_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        album = self._service.find_album_by_name(name)
        return album.put_into_dto() if album else None

    def add_compositor(self, album_name, compositor_name) -> Optional[Dict[str, Any]]:
        return self._service.add_compositor(album_name, compositor_name)

    def get_latest_created_album(self):
        return self._service.get_latest_created_album()

    def reserve_copy(self):
        return self._service.reserve_copy()
