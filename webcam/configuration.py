from typing import Dict, List, Tuple, Optional

import json
import shutil
import datetime
from pathlib import Path

from constants import *
from utils import log, log_error


class Configuration:
    """
    Manages the configurations.
    """
    def __init__(self, path: Path = CONFIGURATION_PATH):
        """
        Loads the data stored in the configuration file as object attributes
        for this instance.
        """
        if not path:
            log("WARNING! The path to the configuration file was set to None. "
                f"Falling back to default: {CONFIGURATION_PATH}")
            path = CONFIGURATION_PATH            
        self.path = path

        # Read the configuration file
        # NOTE: a failure here *should* escalate, don't catch or rethrow
        with open(CONFIGURATION_PATH, 'r') as c:
            configuration = json.load(c)
            configuration = self._decode_json_values(configuration)
        
        # Populate the attributes with the data 
        for key, value in configuration.items():
            setattr(self, key, value)
            
        # Add info about the download time (last edit time)
        last_changed = datetime.timedelta(seconds=CONFIGURATION_PATH.stat().st_mtime)
        self._download_time = datetime.datetime.now() - last_changed
        

    @staticmethod
    def create_from_dictionary(data: Dict, path: Path = CONFIGURATION_PATH) -> 'Configuration':
        """
        Creates a Configuration object starting from a dictionary. Will
        save the configuration file at the specified path.
        """
        data = Configuration._decode_json_values(data)  # Transform strings into numbers
        with open(path, "w+") as d:
            json.dump(data, d, indent=4)
        return Configuration(path)

        
    def __str__(self):
        """
        Prints out as a JSON object
        """
        return json.dumps(vars(self), indent=4, default=lambda x: str(x))


    def backup(self):
        """
        Creates a backup copy of the configuration file.
        """
        try:
            shutil.copy2(self.path, str(self.path) + ".bak")
        except Exception as e:
            log_error("Cannot backup the configuration file.", e)
            log(f"WARNING! The current situation is very fragile, "
                 "please fix this error before a failure occurs.")


    def restore_backup(self):
        """
        Restores the configuration file from its backup copy.
        """
        try:
            shutil.copy2(str(self.path) + ".bak", self.path)
        except Exception as e:
            log_error("Cannot restore the configuration file from its backup.", e)
            log(f"WARNING! The current situation is very fragile, "
                 "please fix this error before a failure occurs.")


    def images_to_download(self) -> List[str]:
        """
        List all the images that are marked as new, 
        aka that they should be redownladed
        """
        to_download = []
        for position, data in self.overlays.items():
            if "changed" in data and data["changed"] == True:
                to_download.append(position)
        return to_download


    @staticmethod
    def _decode_json_values(json: Dict) -> Dict:
        """
        Ensures the JSON is parser properly: converts string numbers and 
        string booleans into the correct types, recursively.
        """
        for key, value in json.items():
            # Recusrion
            if isinstance(value, dict):
                value = Configuration._decode_json_values(value)
            # Check if string boolean
            if isinstance(value, str):
                if value == "false":
                    value = False
                elif value == "true":
                    value = True
                else:
                    # Check if string number
                    try:        
                        value = float(value)
                        value = int(value)
                    except ValueError:
                        pass
            json[key] = value
        return json



