from __future__ import annotations
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from typing import Literal, List, Any
from ..manager.widget_manager import WidgetManager

# QLineEdit + QLabel Layout
def makeLayoutLineEditLabel(
        widget_manager :WidgetManager, 
        key_label      :str,
        key_lineedit   :str, 
        label          :str, 
        axis           :Literal["vertical", "horizontal"] = "vertical", 
        text_set       :str = "", 
        width_fix      :int = 0,
        align          :Qt.AlignmentFlag = Qt.AlignLeft,
        font_family    :str = "Arial", 
        font_size      :int = 12,
        color          :str = "black",
        bold           :bool = False,
        italic         :bool = False
        ) -> QVBoxLayout:
    if axis == "vertical":
        layout = QVBoxLayout()
    elif axis == "horizontal":
        layout = QHBoxLayout()
    else:
        raise ValueError(f"Invalid axis value: {axis}. Expected 'vertical' or 'horizontal'.")
    label_widget = widget_manager.makeWidgetLabel(key_label, label, align, font_family, font_size, color, bold, italic)
    lineedit_widget = widget_manager.makeWidgetLineEdit(key_lineedit, text_set, width_fix)
    label_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    lineedit_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    layout.addWidget(label_widget)
    layout.addWidget(lineedit_widget)
    return layout

# QComboBox + QLabel Layout 
def makeLayoutComboBoxLabel(
        widget_manager :WidgetManager, 
        key_label      :str, 
        key_combobox   :str, 
        label          :str, 
        axis           :Literal["vertical", "horizontal"] = "vertical", 
        items          :List[str] = [], 
        idx_default    :int = 0,
        align          :Qt.AlignmentFlag = Qt.AlignLeft, 
        font_family    :str = "Arial", 
        font_size      :int = 12, 
        color          :str = "black", 
        bold           :bool = False, 
        italic         :bool = False
        ) -> QVBoxLayout:
    if axis == "vertical":
        layout = QVBoxLayout()
    elif axis == "horizontal":
        layout = QHBoxLayout()
    else:
        raise ValueError(f"Invalid axis value: {axis}. Expected 'vertical' or 'horizontal'.")
    label_widget = widget_manager.makeWidgetLabel(key_label, label, align, font_family, font_size, color, bold, italic)
    combobox_widget = widget_manager.makeWidgetComboBox(key_combobox, items, idx_default)
    layout.addWidget(label_widget)
    layout.addWidget(combobox_widget)
    return layout

# QButtonGroup Layout
def makeLayoutButtonGroup(
        q_widget: QWidget, 
        widget_manager: WidgetManager, 
        key_buttongroup: str, 
        list_label_buttongroup: List[str], 
        set_exclusive: bool=True, 
        idx_check: int=0
        ) -> QHBoxLayout:
    layout = QHBoxLayout()
    button_group = QButtonGroup(q_widget)
    button_group.setExclusive(set_exclusive)

    for i, label_buttongroup in enumerate(list_label_buttongroup):
        radio_button = QRadioButton(label_buttongroup)
        if i == idx_check:  # idx_check番目にチェック
            radio_button.setChecked(True)
        layout.addWidget(radio_button)
        button_group.addButton(radio_button, i)

    widget_manager.dict_buttongroup[key_buttongroup] = button_group
    return layout

# QSlider + QLabel Layout
def makeLayoutSliderLabel(
        widget_manager: WidgetManager, 
        key_label: str, 
        key_slider: str, 
        label: str, 
        axis :Literal["vertical", "horizontal"] = "vertical", 
        align: Qt.AlignmentFlag=Qt.AlignLeft, 
        func_: Any=None, 
        value_min: int=0, 
        value_max: int=255, 
        value_set: int=10, 
        height: int=10, 
        axis_slider: Qt.Orientation=Qt.Horizontal
    ) -> QVBoxLayout:
    if axis == "vertical":
        layout = QVBoxLayout()
    elif axis == "horizontal":
        layout = QHBoxLayout()
    else:
        raise ValueError(f"Invalid axis value: {axis}. Expected 'vertical' or 'horizontal'.")
    label_widget = widget_manager.makeWidgetLabel(key_label, label, align)
    slider_widget = widget_manager.makeWidgetSlider(key_slider, func_, value_min, value_max, value_set, height, axis_slider)
    layout.addWidget(label_widget)
    layout.addWidget(slider_widget)
    return layout

# QSpinBox + QLabel Layout
def makeLayoutSpinBoxLabel(
        widget_manager: WidgetManager, 
        key_label: str, 
        key_spinbox: str, 
        label: str, 
        axis: Literal["vertical", "horizontal"]="vertical",
        align: Qt.AlignmentFlag=Qt.AlignLeft, 
        value_min: int=1, 
        value_max: int=100, 
        value_set: int=5,
        step: int=1,
        ) -> QVBoxLayout:
    if axis == "vertical":
        layout = QVBoxLayout()
    elif axis == "horizontal":
        layout = QHBoxLayout()
    else:
        raise ValueError(f"Invalid axis value: {axis}. Expected 'vertical' or 'horizontal'.")
    label_widget = widget_manager.makeWidgetLabel(key_label, label, align)
    spinner_widget = widget_manager.makeWidgetSpinBox(key_spinbox, value_min, value_max, value_set, step)
    layout.addWidget(label_widget)
    layout.addWidget(spinner_widget)
    return layout