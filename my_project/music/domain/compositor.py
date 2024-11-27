from __future__ import annotations

from typing import Dict, Any
from .i_dto import IDto
from my_project import db


class Compositor(db.Model, IDto):
    __tablename__ = "compositor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(75))
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=True)
    label = db.relationship("Label")

    albums = db.relationship(
        "Album",
        secondary="compositor_album",
        back_populates="compositors"
    )

    def __repr__(self) -> str:
        return f"Compositor({self.id}, '{self.name}', '{self.label}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "label_id": self.label_id or "",
            "label": self.label.name if self.label is not None else "",
            "albums": [{"id": album.id, "name": album.name} for album in self.albums]
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Compositor:
        obj = Compositor(**dto_dict)
        return obj
