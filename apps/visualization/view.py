from __future__ import annotations
from typing import Any, Dict, List, Tuple
from ..control import ViewControl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import numpy as np

# BaslerCameraGUI update view
def updateView_BaslerCameraGUI(
    view_control: ViewControl,
    im: np.ndarray[int, int, int],
):
    height, width, _ = im.shape
    qimage = QImage(im, width, height, width * 3, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
    view_control.dict_layer["camera"].setPixmap(pixmap)
    # set aspect ratio
    view_control.q_view.fitInView(view_control.q_view.sceneRect(), Qt.KeepAspectRatio)