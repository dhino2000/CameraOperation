from __future__ import annotations
from typing import Dict
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from ..manager import WidgetManager, ControlManager, DataManager, ConfigManager

class ViewControl:
    def __init__(
            self, 
            q_view          : QGraphicsView, 
            q_scene         : QGraphicsScene, 
            data_manager    : DataManager, 
            widget_manager  : WidgetManager, 
            config_manager  : ConfigManager, 
            control_manager : ControlManager,
        ):
        self.q_view          = q_view
        self.q_scene         = q_scene
        self.data_manager    = data_manager
        self.widget_manager  = widget_manager
        self.config_manager  = config_manager
        self.control_manager = control_manager
        # self.view_handler    = ViewHandler(self, app_key)

        self.current_app = self.config_manager.current_app

        self.initializeViewLayer()

    # update view
    def updateView(self) -> None:
        if self.current_app == "BaslerCameraGUI":
            from ..visualization.view import updateView_BaslerCameraGUI
            updateView_BaslerCameraGUI(self, self.data_manager.im)

    # initialize view layer
    def initializeViewLayer(self) -> None:
        self.dict_layer: Dict[str, QGraphicsPixmapItem] = {}
        # set scene to view
        self.q_view.setScene(self.q_scene)

    # add view layer
    def addViewLayer(self, key: str) -> None:
        layer = QGraphicsPixmapItem()
        self.q_scene.addItem(layer)
        self.dict_layer[key] = layer

