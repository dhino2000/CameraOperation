from __future__ import annotations
from typing import Dict
from PyQt5.QtWidgets import QLineEdit
from pypylon import pylon
import numpy as np

"""
Balser Camera Capture
"""
# get camera config
# fps, width, height, offsetx, offsety, gain, exposure
def getCameraConfigDict(dict_lineedit: Dict[str, QLineEdit]) -> Dict[str, float]:
    dict_camera_config = {
        "fps": float(dict_lineedit["fps"].text()),
        "width": int(dict_lineedit["width"].text()),
        "height": int(dict_lineedit["height"].text()),
        "offset_x": int(dict_lineedit["offset_x"].text()),
        "offset_y": int(dict_lineedit["offset_y"].text()),
        "gain": float(dict_lineedit["gain"].text()),
        "exposure_time": int(dict_lineedit["exposure_time"].text())
    }
    return dict_camera_config
    
# カメラの準備
def setCamera(
        camera: pylon.InstantCamera, 
        converter: pylon.ImageFormatConverter,  
        dict_camera_config: Dict[str, float]
        ) -> None:
    camera.AcquisitionFrameRateEnable.SetValue(True)
    camera.AcquisitionFrameRate.SetValue(dict_camera_config["fps"]) # FPS
    camera.OffsetX = dict_camera_config["offset_x"]
    camera.OffsetY = dict_camera_config["offset_y"]
    camera.Width = dict_camera_config["width"]
    camera.Height = dict_camera_config["height"]
    camera.Gain = dict_camera_config["gain"]
    camera.ExposureTime.SetValue(dict_camera_config["exposure_time"])

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_Mono8
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# 画像を1枚取得
def singleCapture(
        camera: pylon.InstantCamera, 
        converter: pylon.ImageFormatConverter, 
        dict_lineedit: Dict[str, QLineEdit]
        ) -> np.ndarray[int, int]:
    # カメラセット
    camera.Open()
    dict_camera_config = getCameraConfigDict(dict_lineedit)
    setCamera(camera, converter, dict_camera_config)

    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    image = converter.Convert(grabResult)
    img = image.GetArray()
    grabResult.Release()
    camera.StopGrabbing()
    camera.Close()
    return img