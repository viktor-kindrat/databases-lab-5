from __future__ import annotations

from .general_dao import GeneralDAO
from my_project.music.domain import Genre

from sqlalchemy import text


class GenreDAO(GeneralDAO):
    _domain_type = Genre

    def create(self, obj: Genre) -> Genre:
        sql = text("""
                    CALL insert_into_table(
                        :table_name,
                        :column_list,
                        :value_list
                    )
                """)

        params = {
            "table_name": "genre",
            "column_list": "name, description",
            "value_list": f"'{obj.name}', '{obj.description}'"
        }

        self._session.execute(sql, params)
        self._session.commit()

        return obj

    def create_noname_genres(self):
        self._session.execute(text("CALL insert_noname('genre')"), {})
        return self._session.commit()
