from __future__ import annotations
from typing import Dict, Any
from my_project import db
from .i_dto import IDto


class Genre(db.Model, IDto):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"Genre({self.id}, '{self.name}', '{self.description}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Genre:
        return Genre(**dto_dict)