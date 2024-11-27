from .general_service import GeneralService
from my_project.music.dao import album_dao


class AlbumService(GeneralService):
    _dao = album_dao

    def find_album_by_name(self, name: str):
        return self._dao.find_by_name(name)

    def add_compositor(self, album_name, compositor_name):
        return self._dao.add_compositor(album_name, compositor_name)

    def get_latest_created_album(self):
        return self._dao.get_latest_created_album()

    def reserve_copy(self):
        return self._dao.reserve_copy()
