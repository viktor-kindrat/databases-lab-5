from my_project.music.dao import genre_dao
from .general_service import GeneralService


class GenreService(GeneralService):
    _dao = genre_dao

    def create_noname_genres(self):
        self._dao.create_noname_genres()

