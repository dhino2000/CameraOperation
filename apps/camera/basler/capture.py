from __future__ import annotations
from typing import Dict, List, Tuple
from PyQt5.QtWidgets import QLineEdit
from pypylon import pylon
import numpy as np
import cv2
import time

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
        ) -> Tuple[pylon.InstantCamera, pylon.ImageFormatConverter]:
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
    return camera, converter

# キャプチャ開始
def startCapture(        
        camera: pylon.InstantCamera, 
        converter: pylon.ImageFormatConverter, 
        dict_camera_config: Dict[str, float]
        ) -> Tuple[pylon.InstantCamera, pylon.ImageFormatConverter]:
    # カメラセット
    camera.Open()
    camera, converter = setCamera(camera, converter, dict_camera_config)
    return camera, converter

# キャプチャ終了
def stopCapture(
        camera: pylon.InstantCamera, 
) -> pylon.InstantCamera:
    camera.StopGrabbing()
    camera.Close()
    return camera

# 画像取得
def captureImage(
        camera: pylon.InstantCamera, 
        converter: pylon.ImageFormatConverter, 
) -> np.ndarray[int, int]:
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        image = converter.Convert(grabResult)
        img = image.GetArray()
    grabResult.Release()
    return img
    
# 画像を1枚取得
def singleCapture(
        camera: pylon.InstantCamera, 
        converter: pylon.ImageFormatConverter, 
        dict_camera_config: Dict[str, float]
        ) -> np.ndarray[int, int]:
    camera, converter = startCapture(camera, converter, dict_camera_config)
    # only single capture
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    img = captureImage(camera, converter)
    camera = stopCapture(camera)
    return img

# カメラの連続撮影、別ウィンドウに表示
def continuousCapture(
    camera: pylon.InstantCamera, 
    converter: pylon.ImageFormatConverter, 
    dict_camera_config: Dict[str, float],
    cv2_window_name: str = "",
    video_writer: cv2.VideoWriter = None,
    return_timestamps: bool = False,
    key_id: int = 27,  # Esc key
) -> List[float]:
    camera, converter = startCapture(camera, converter, dict_camera_config)
    
    # 時間計測用配列
    list_t = []
    
    # キャプチャフラグ
    capture_flag = True
    
    # 連続キャプチャ開始
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    
    while capture_flag:
        img = captureImage(camera, converter)
            
        # OpenCVウィンドウに表示
        if cv2_window_name != "":
            cv2.imshow(cv2_window_name, img)
        # 動画に画像書き込み
        if video_writer is not None:
            video_writer.write(img)
        
        # 時間記録
        t = time.time()
        list_t.append(t)
        
        # Escキーでキャプチャ終了
        key = cv2.waitKey(1)
        if key == key_id:
            capture_flag = False
        
    # リソース解放
    stopCapture(camera)
    cv2.destroyAllWindows()
    if return_timestamps:
        return list_t
    else:
        return
