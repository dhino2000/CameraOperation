from ..manager import WidgetManager, ControlManager, DataManager
from PyQt5.QtWidgets import QPushButton, QWidget
from ..camera.basler.capture import singleCapture
import cv2

# widget_manager.dict_button["capture_single"]
def bindFuncButtonCaptureSingle(
    q_button: QPushButton, 
    q_window: QWidget,
    widget_manager: WidgetManager,
    control_manager: ControlManager,
    data_manager: DataManager,
) -> None:
    camera = control_manager.camera
    converter = control_manager.converter
    # hardcoded !!!
    dict_lineedit = {config: widget_manager.dict_lineedit[config] for config in 
                     ["fps", "width", "height", "offset_x", "offset_y", "gain", "exposure_time"]}

    q_button.clicked.connect(lambda: _singleCapture(camera, converter, dict_lineedit, data_manager))

    def _singleCapture(camera, converter, dict_lineedit, data_manager):
        im = singleCapture(camera, converter, dict_lineedit)
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB) # mono to bgr
        data_manager.im = im
        control_manager.view_control.updateView()

                             