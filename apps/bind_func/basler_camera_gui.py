from ..manager import WidgetManager, ControlManager, DataManager
from ..control import ViewControl, BaslerCameraControl, ConnectorControl
from PyQt5.QtWidgets import QPushButton, QWidget
import cv2

# widget_manager.dict_button["capture_single"]
def bindFuncButtonCaptureSingle(
    q_button: QPushButton, 
    q_window: QWidget,
    widget_manager: WidgetManager,
    camera_control: BaslerCameraControl,
    view_control: ViewControl,
) -> None:
    # hardcoded !!!
    dict_lineedit = {config: widget_manager.dict_lineedit[config] for config in 
                     ["fps", "width", "height", "offset_x", "offset_y", "gain", "exposure_time"]}

    q_button.clicked.connect(lambda: _singleCapture(camera_control, dict_lineedit))

    def _singleCapture(camera_control: BaslerCameraControl, dict_lineedit):
        camera_control.setDictCameraConfigFromDictLineEdit(dict_lineedit)
        camera_control.singleCapture(is_convert_mono_to_color=True)
        view_control.updateView()

# widget_manager.dict_button["play"]
def bindFuncButtonPlay(
    q_button: QPushButton, 
    q_window: QWidget,
    widget_manager: WidgetManager,
    camera_control: BaslerCameraControl,
) -> None:
    # hardcoded !!!
    dict_lineedit = {config: widget_manager.dict_lineedit[config] for config in 
                     ["fps", "width", "height", "offset_x", "offset_y", "gain", "exposure_time"]}

    q_button.clicked.connect(lambda: _continuousCapture(camera_control, dict_lineedit))

    def _continuousCapture(camera_control: BaslerCameraControl, dict_lineedit):
        camera_control.setDictCameraConfigFromDictLineEdit(dict_lineedit)
        # ウィンドウ作成
        cv2_window_name = "Esc: Stop capture"
        key_id = 27
        cv2.namedWindow(cv2_window_name)
        camera_control.onlyContinuousCapture(cv2_window_name, key_id)