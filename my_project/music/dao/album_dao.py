from __future__ import annotations

from .general_dao import GeneralDAO
from my_project.music.domain import Album
from my_project.music.domain import Compositor
from sqlalchemy.orm import Session
from sqlalchemy import text


class AlbumDAO(GeneralDAO):
    _domain_type = Album

    def find_by_name(self, name: str) -> Album | None:
        return self._session.query(self._domain_type).filter_by(name=name).first()

    def add_compositor(self, album_name, compositor_name) -> None:
        sql = text("CALL insert_compositor_album(:compositor_name, :album_name)")

        params = {
            "compositor_name": compositor_name,
            "album_name": album_name,
        }

        print(compositor_name, album_name)

        self._session.execute(sql, params)
        return self._session.commit()

    def get_latest_created_album(self) -> Album | None:
        # Call the procedure
        sql = text("CALL column_aggregate_procedure('album', 'created_at', 'MAX')")

        result = self._session.execute(sql, {})

        latest_created_at = result.fetchone()

        if latest_created_at:
            latest_created_at_value = latest_created_at[0]

            latest_album = self._session.query(self._domain_type).filter_by(created_at=latest_created_at_value).first()
            return latest_album

        return None

    def reserve_copy(self) -> bool:
        sql = text("CALL split_table_dynamic()")

        self._session.execute(sql, {})
        self._session.commit()

        return True


