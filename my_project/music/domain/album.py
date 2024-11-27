from __future__ import annotations
from typing import Dict, Any
from .i_dto import IDto
from my_project import db


class Album(db.Model, IDto):
    __tablename__ = "album"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    genre_id = db.Column(db.Integer, nullable=False)

    compositors = db.relationship(
        "Compositor",
        secondary="compositor_album",
        back_populates="albums"
    )

    def __repr__(self) -> str:
        return f"Album({self.id}, '{self.name}', '{self.created_at}', '{self.genre_id}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "genre_id": self.genre_id,
            "compositors": [{"id": compositor.id, "name": compositor.name} for compositor in self.compositors]
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Album:
        return Album(**dto_dict)
