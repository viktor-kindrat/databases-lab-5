from __future__ import annotations

from typing import Dict, Any
from .i_dto import IDto
from my_project import db


class Label(db.Model, IDto):
    __tablename__ = "label"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(75))
    compositors = db.relationship("Compositor", lazy="dynamic", viewonly=True)

    def __repr__(self) -> str:
        return f"Label({self.id}, '{self.name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Label:
        obj = Label(**dto_dict)
        return obj
