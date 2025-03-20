from __future__ import annotations
from PyQt5.QtWidgets import QPushButton, QWidget
from ..utils.app_utils import exitApp

# -> widget_manager.dict_button["exit"]
def bindFuncExit(
    q_button: 'QPushButton', 
    q_window: 'QWidget'
) -> None:
    q_button.clicked.connect(lambda: exitApp(q_window))