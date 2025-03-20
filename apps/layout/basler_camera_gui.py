from __future__ import annotations
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from ..manager.widget_manager import WidgetManager
from .base_layouts import makeLayoutLineEditLabel

"""
Main Layouts
"""
def makeLayoutBaslerCameraGUI(widget_manager, config_manager):
    layout = QGridLayout()
    # left and right layout
    layout_left = QVBoxLayout()
    layout_right = QVBoxLayout()

    layout_left.addLayout(makeLayoutMovieSaveAndMoveDestination(
        widget_manager, 
        "path_config",
        "dir_movie_save",
        "dst_movie_move",
        "dir_movie_save",
        "dst_movie_move",
        "movie_save",
        "movie_move",
        config_manager.config["savedir_camera"],
        config_manager.config["movedst_camera"],
    ))
    layout_left.addLayout(makeLayoutCameraConfig(
        widget_manager, 
        "camera_config",
        "fps",
        "width",
        "height",
        "offset_x",
        "offset_y",
        "gain",
        "exposure_time",
        "fps",
        "width",
        "height",
        "offset_x",
        "offset_y",
        "gain",
        "exposure_time",
    ))
    layout_left.addLayout(makeLayoutCameraOperation(
        widget_manager,
        "camera_operation",
        "capture_single",
        "play",
        "capture_movie",
        "start",
        "move_movie",
        "exit",
    ))

    layout_right.addLayout(makeLayoutCameraView(widget_manager, "view_camera"))

    layout.addLayout(layout_left, 0, 0)
    layout.addLayout(layout_right, 0, 1, 1, 3)

    return layout

"""
Sub Layouts
"""
# movie save directory, moving destination directory
def makeLayoutMovieSaveAndMoveDestination(
        widget_manager :WidgetManager, 
        key_label_path_config :str,
        key_label_movie_save :str,
        key_label_movie_move :str,
        key_lineedit_movie_save :str, 
        key_lineedit_movie_move :str,
        key_button_movie_save :str,
        key_button_movie_move :str, 
        text_set_movie_save :str, 
        text_set_movie_move :str, 
        width_fix :int = 0,
        ) -> QGridLayout:
    layout = QGridLayout()
    align = Qt.AlignCenter
    label_path_config = widget_manager.makeWidgetLabel(key_label_path_config, "Path Config", align=align)
    label_movie_save = widget_manager.makeWidgetLabel(key_label_movie_save, "Save Directory:", align=align)
    label_movie_move = widget_manager.makeWidgetLabel(key_label_movie_move, "Move Destination:", align=align)
    lineedit_movie_save = widget_manager.makeWidgetLineEdit(key_lineedit_movie_save, text_set_movie_save, width_fix)
    lineedit_movie_move = widget_manager.makeWidgetLineEdit(key_lineedit_movie_move, text_set_movie_move, width_fix)
    button_movie_save = widget_manager.makeWidgetButton(key_button_movie_save, "browse")
    button_movie_move = widget_manager.makeWidgetButton(key_button_movie_move, "browse")
    layout.addWidget(label_path_config, 0, 0, 1, 3)
    layout.addWidget(label_movie_save, 1, 0)
    layout.addWidget(lineedit_movie_save, 1, 1)
    layout.addWidget(button_movie_save, 1, 2)
    layout.addWidget(label_movie_move, 2, 0)
    layout.addWidget(lineedit_movie_move, 2, 1)
    layout.addWidget(button_movie_move, 2, 2)
    return layout

# camera config
def makeLayoutCameraConfig(
        widget_manager :WidgetManager, 
        key_label_camera_config :str,
        key_label_fps :str,
        key_label_width :str,
        key_label_height :str,
        key_label_offset_x :str,
        key_label_offset_y :str,
        key_label_gain :str,
        key_label_exposure :str,
        key_lineedit_fps :str,
        key_lineedit_width :str,
        key_lineedit_height :str,
        key_lineedit_offset_x :str,
        key_lineedit_offset_y :str,
        key_lineedit_gain :str,
        key_lineedit_exposure :str,
        ) -> QVBoxLayout:
    layout = QVBoxLayout()
    align = Qt.AlignCenter
    layout.addWidget(widget_manager.makeWidgetLabel(key_label_camera_config, "Camera Config", align=align), 1)
    # hardcoded !!!
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_fps, key_lineedit_fps, "FPS", "horizontal", "60.0", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_width, key_lineedit_width, "Width", "horizontal", "1280", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_height, key_lineedit_height, "Height", "horizontal", "1024", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_offset_x, key_lineedit_offset_x, "Offset X", "horizontal", "0", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_offset_y, key_lineedit_offset_y, "Offset Y", "horizontal", "0", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_gain, key_lineedit_gain, "Gain", "horizontal", "12.0", align=align), 1)
    layout.addLayout(makeLayoutLineEditLabel(widget_manager, key_label_exposure, key_lineedit_exposure, "Exposure Time (μs)", "horizontal", "2000", align=align), 1)
    return layout

# camera operation
def makeLayoutCameraOperation(
        widget_manager :WidgetManager,
        key_label_camera_operation :str,
        key_button_capture_single :str,
        key_button_play :str,
        key_button_capture_movie :str,
        key_button_start :str,
        key_button_move_movie :str,
        key_button_exit :str,
):
    layout = QVBoxLayout()
    layout_1 = QHBoxLayout()
    layout_2 = QHBoxLayout()
    layout_3 = QHBoxLayout()
    label_camera_operation = widget_manager.makeWidgetLabel(key_label_camera_operation, "Camera Operation", align=Qt.AlignCenter)
    layout_1.addWidget(widget_manager.makeWidgetButton(key_button_capture_single, "Capture Single"))
    layout_1.addWidget(widget_manager.makeWidgetButton(key_button_play, "Play"))
    layout_1.addWidget(widget_manager.makeWidgetButton(key_button_capture_movie, "Capture Movie"))
    layout_2.addWidget(widget_manager.makeWidgetButton(key_button_start, "Start Capture with Bpod"))
    layout_3.addWidget(widget_manager.makeWidgetButton(key_button_move_movie, "Move Video Files"))
    layout_3.addWidget(widget_manager.makeWidgetButton(key_button_exit, "Exit"))
    
    layout.addWidget(label_camera_operation)
    layout.addLayout(layout_1)
    layout.addLayout(layout_2)
    layout.addLayout(layout_3)
    return layout

# camera view
def makeLayoutCameraView(
        widget_manager :WidgetManager,
        key_view :str,
):
    layout = QVBoxLayout()
    layout.addWidget(widget_manager.makeWidgetView(key_view, width_min=1280, height_min=1024)) # hardcoded !!!
    return layout