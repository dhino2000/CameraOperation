# USBカメラ、Baslerカメラ制御用の関数
from pypylon import pylon
from PIL import Image, ImageTk
import tkinter as tk
"""
USB Camera
"""

"""
Basler Camera
"""
# カメラのコンフィグをdictとして取得
def getCameraConfigDict(gui):
    gui.camera_config_dict = {}

    gui.camera_config_dict["fps"] = float(gui.entry_dict["fps"].get())
    gui.camera_config_dict["width"] = int(gui.entry_dict["width"].get())
    gui.camera_config_dict["height"] = int(gui.entry_dict["height"].get())
    gui.camera_config_dict["offsetx"] = int(gui.entry_dict["offsetx"].get())
    gui.camera_config_dict["offsety"] = int(gui.entry_dict["offsety"].get())
    gui.camera_config_dict["gain"] = float(gui.entry_dict["gain"].get())
    gui.camera_config_dict["exposure_time"] = int(gui.entry_dict["exposure_time"].get())

# カメラの準備
def setCamera(gui):
    # コンフィグ設定
    camera_config = gui.camera_config_dict

    gui.camera.AcquisitionFrameRateEnable.SetValue(True)
    gui.camera.AcquisitionFrameRate.SetValue(camera_config["fps"]) # FPS
    gui.camera.OffsetX = camera_config["offsetx"]
    gui.camera.OffsetY = camera_config["offsety"]
    gui.camera.Width = camera_config["width"]
    gui.camera.Height = camera_config["height"]
    gui.camera.Gain = camera_config["gain"]
    gui.camera.ExposureTime.SetValue(camera_config["exposure_time"])

    # converting to opencv bgr format
    gui.converter = pylon.ImageFormatConverter()
    gui.converter.OutputPixelFormat = pylon.PixelType_Mono8
    gui.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# 画像を1枚取得
def singleCapture(gui):
    # カメラセット
    gui.camera.Open()
    getCameraConfigDict(gui)
    setCamera(gui)

    gui.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    grabResult = gui.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    image = gui.converter.Convert(grabResult)
    img = image.GetArray()
    grabResult.Release()
    gui.camera.StopGrabbing()
    gui.camera.Close()
    return img

# 画像を1枚取得してを表示Imageに表示
def singleCaptureAndShow(gui, canvas):
    image = singleCapture(gui)
    # arrayをPIL形式に変更してさらにTKinter PhotoImageに変換
    frame = image
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)

    # canvasに画像を表示
    canvas.config(width=frame.width(), height=frame.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=frame)
    canvas.image = frame

# 選択範囲で画像クロップ
def cropImage(img, cropcoords):
    if len(cropcoords) > 0:
        img = img[cropcoords[2]:cropcoords[3], cropcoords[0]:cropcoords[1]]
    return img
