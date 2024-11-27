from __future__ import annotations
from .general_dao import GeneralDAO

from my_project import db
from my_project.music.domain import Compositor
from my_project.music.domain import Album


class CompositorDAO(GeneralDAO):
    _domain_type = Compositor

    def find_by_name(self, name: str) -> Compositor | None:
        """Find a Compositor by name."""
        return self._session.query(self._domain_type).filter_by(name=name).first()

    def add_album(self, compositor_id: int, album_id: int):
        compositor = self.find_by_id(compositor_id)
        album = db.session.query(Album).get(album_id)

        if compositor and album:
            compositor.albums.append(album)
            db.session.commit()
        else:
            raise ValueError("Compositor or Album not found")
