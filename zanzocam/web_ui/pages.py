import os
import shutil
from datetime import datetime
from typing import OrderedDict

from flask import render_template

from zanzocam.web_ui.utils import read_network_data, read_setup_data_file, read_flag_file, read_log_file, clear_logs
from zanzocam.webcam.system import get_wifi_data
from zanzocam.constants import *



def home_page():
    """ The initial page with the summary """
    hotspot_value = read_flag_file(HOTSPOT_FLAG, "YES")
    network_data = read_network_data()
    network_data["wifi_data"] = get_wifi_data()
    server_data = read_setup_data_file(CONFIGURATION_FILE).get('server', {})
    return render_template("home.html", 
                            title="Setup", 
                            version=VERSION, 
                            hotspot_value=hotspot_value,
                            network_data=network_data,
                            server_data=server_data)

def network_page():
    """ The page with the network forms """
    network_data = read_network_data()
    return render_template("network.html", 
                            title="Setup Rete", 
                            version=VERSION,
                            network_data=network_data)

def server_page():
    """ The page with the server data forms """
    server_data = read_setup_data_file(CONFIGURATION_FILE).get('server', {})
    return render_template("server.html", 
                            title="Setup Server", 
                            version=VERSION,
                            server_data=server_data)

def webcam_page():
    """ The page where a picture can be shoot """
    clear_logs(PICTURE_LOGS)  # To not see old logs in the textarea
    return render_template("webcam.html", 
                           title="Setup Webcam", 
                           version=VERSION,
                           preview_url=PREVIEW_PICTURE_URL)


def logs_page():
    """ The page with the logs browser """
    logs = OrderedDict()

    if CAMERA_LOGS.is_dir():
        
        # Sort by edit time
        log_files = [name for name in os.listdir(CAMERA_LOGS) if "camera" not in name]
        sorted_logs = sorted(log_files, key=lambda name:datetime.strptime(name, LOG_NAME_FORMAT), reverse=True)

        for logfile in sorted_logs:
            if logfile.startswith("logs"):
                logs[Path(logfile).name] = {
                    "date": datetime.strptime(logfile, LOG_NAME_FORMAT),
                    "content": read_log_file(CAMERA_LOGS / logfile)
                }
        total_logs_size = sum(file.stat().st_size for file in Path(CAMERA_LOGS).rglob('*')) 
        _, _, free_disk_space = shutil.disk_usage(__file__)
        percentage_occupancy = (total_logs_size / (total_logs_size + free_disk_space)) * 100

        no_logs_dir = False
        logs_count=len(logs.keys())
        logs_size=f"{(total_logs_size / 1024):.2f} KB"
        log_disk_occupancy=f"{percentage_occupancy:.4f}%"

    else:
        no_logs_dir = True
        logs=[]
        logs_count=0
        logs_size="0 KB"
        log_disk_occupancy="0.0000%"

    return render_template("logs.html",
                            title="Logs",
                            version=VERSION,
                            no_logs_dir=no_logs_dir,
                            logs=logs,
                            logs_count=logs_count,
                            logs_size=logs_size,
                            log_disk_occupancy=log_disk_occupancy)
