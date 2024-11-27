from .general_dao import GeneralDAO

from my_project.label.domain.label import Label


class LabelDAO(GeneralDAO):
    _domain_type = Label
