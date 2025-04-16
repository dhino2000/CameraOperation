from __future__ import annotations
from typing import Dict, List, Optional
from PyQt5.QtWidgets import QLineEdit
from pypylon import pylon
from ..manager import DataManager
from ..camera.basler.capture import singleCapture, continuousCapture, getCameraConfigDict, setCamera
import cv2
import numpy as np

# Camera control class for Basler camera
class BaslerCameraControl:
    def __init__(
            self, 
            data_manager: DataManager,
            camera: pylon.InstantCamera,
            converter: pylon.ImageFormatConverter,
            ):
        self.data_manager = data_manager
        self.camera = camera
        self.converter = converter
        self.dict_camera_config: Dict[str, float] = {}
        self.dict_flag: Dict[str, bool] = {}

    """
    initalize functions
    """
    def initDataManager(self) -> None:
        self.data_manager.im = None
        self.data_manager.list_t = []

    def initCamera(self):
        self.camera, self.converter = setCamera(self.camera, self.converter, self.dict_camera_config)

    """
    get functions
    """
    def getFlag(self, key: str) -> bool:
        return self.dict_flag.get(key)
    
    def getImage(self) -> np.ndarray[int, int]:
        return self.data_manager.im
    
    """
    set functions
    """
    def setFlag(self, key: str, flag: bool) -> None:
        self.dict_flag[key] = flag

    def setDictCameraConfigFromDictLineEdit(self, dict_lineedit: Dict[str, QLineEdit]) -> None:
        self.dict_camera_config = getCameraConfigDict(dict_lineedit)
        
    def singleCapture(self, is_convert_mono_to_color: bool = False):
        img = singleCapture(self.camera, self.converter, self.dict_camera_config)
        if is_convert_mono_to_color:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) # mono to bgr
        self.data_manager.im = img
        
    def onlyContinuousCapture(
            self, 
            cv2_window_name: str = "Esc: Stop capture",
            key_id: int=27
            ) -> None:
        continuousCapture(
            camera=self.camera, 
            converter=self.converter, 
            dict_camera_config=self.dict_camera_config, 
            cv2_window_name=cv2_window_name,
            key_id=key_id,  # Esc key
            )
    