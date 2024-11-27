from .general_service import GeneralService
from my_project.label.dao import label_dao


class LabelService(GeneralService):
    _dao = label_dao

