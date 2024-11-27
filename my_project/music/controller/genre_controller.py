from .general_controller import GeneralController

from my_project.music.service import genre_service


class GenreController(GeneralController):
    _service = genre_service

    def create_noname_genres(self):
        return self._service.create_noname_genres()
