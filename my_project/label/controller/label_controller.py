from my_project.label.service import label_service
from my_project.label.controller.general_controller import GeneralController


class LabelController(GeneralController):
    _service = label_service

