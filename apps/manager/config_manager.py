from __future__ import annotations
from pathlib import Path
import os
import sys
import socket
import importlib.util

class ConfigManager:
    def __init__(self, path_config: str = "./config.py"):
        self.current_app       : str = None
        self.current_dir       : str = os.path.dirname(os.path.abspath("__file__"))
        self.path_config       : str = path_config
        self.hostname          : str = socket.gethostname()

        self.config            : dict = self.loadConfig()

    def loadConfig(self):
        path_config_norm = os.path.normpath(os.path.join(self.current_dir, self.path_config))
        spec = importlib.util.spec_from_file_location("config_module", path_config_norm)
        config_module = importlib.util.module_from_spec(spec)
        sys.modules["config_module"] = config_module
        spec.loader.exec_module(config_module)
        dict_config = config_module.dict_config
        config = dict_config[self.hostname]
        return config