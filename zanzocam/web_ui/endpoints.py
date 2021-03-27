import sys
import logging
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, request

import constants
from web_ui import pages, api


app = Flask(__name__)

# Setup the logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(constants.SERVER_LOG),
        logging.StreamHandler(sys.stdout),
    ]
)


#
# Pages
#

@app.route("/", methods=["GET"])
def home_endpoint(feedback: str=None, feedback_sheet_name: str=None, feedback_type: str=None):
    if feedback_type=="positive":
        return_code = 200
    else:
        return_code = 200
    return pages.home(feedback=feedback, 
                      feedback_sheet_name=feedback_sheet_name, 
                      feedback_type=feedback_type), return_code

@app.route("/webcam-setup", methods=["GET"])
def webcam_endpoint():
    return pages.webcam()


@app.route("/webcam-calibration", methods=['GET'])
def low_light_calibration_endpoint():
    return pages.low_light_calibration()



#
# API for setting configuration values
#

@app.route("/configure/wifi", methods=["POST"])
def configure_wifi_endpoint():
    feedback = api.configure_wifi(request.form)
    if feedback == "":
        return redirect(url_for('home_endpoint', feedback="Wifi configurato con successo", feedback_sheet_name="wifi", feedback_type="positive")), 20
    return redirect(url_for('home_endpoint', feedback=feedback, feedback_sheet_name="wifi", feedback_type="negative"))
    

@app.route("/configure/server", methods=["POST"])
def configure_server_endpoint():
    feedback = api.configure_server(request.form)
    if feedback == "":
        return redirect(url_for('home_endpoint', feedback="Dati server configurati con successo", feedback_sheet_name="server", feedback_type="positive"))
    return redirect(url_for('home_endpoint', feedback=feedback, feedback_sheet_name="server", feedback_type="negative"))
    

@app.route("/configure/hotspot/<value>", methods=["POST"])
def toggle_hotspot_endpoint(value):
    return api.toggle_hotspot(value)


@app.route("/configure/low-light-calibration/<value>", methods=["POST"])
def toggle_calibration_endpoint(value):
    return api.toggle_calibration(value)


@app.route("/configure/low-light-calibration-data", methods=['POST'])
def save_calibration_data_endpoint():
    data = request.form.get('calibration-data')
    api.save_calibration_data(data)
    return redirect(url_for('low_light_calibration_endpoint'))


@app.route("/configure/low-light-calibrated_values", methods=['GET'])
def apply_calibrated_values_endpoint():
    feedback = api.apply_calibrated_values(request.args)
    if feedback == "":
        return redirect(url_for('low_light_calibration_endpoint', feedback="Valori impostati con successo."))
    return redirect(url_for('low_light_calibration_endpoint', feedback=feedback))


#
# API to take actions
#

@app.route("/shoot-picture", methods=["POST"])
def shoot_picture_endpoint():
    return "", api.shoot_picture()


#
# API to fetch data
#

@app.route("/preview-picture", methods=["GET"])
def get_preview_endpoint():
    return api.get_preview()


@app.route("/logs/<kind>/<name>", methods=["GET"])
def get_logs_endpoint(kind: str, name: str):
    return api.get_logs(kind, name)
    

#
# Error handlers
#

@app.errorhandler(400)
def handle_bad_request(e):
    return render_template("error.html", title="400", message="400 - Bad Request"), 400

@app.errorhandler(401)
def handle_unauthorized(e):
    return render_template("error.html", title="401", message="401 - Unauthorized"), 401

@app.errorhandler(403)
def handle_forbidden(e):
    return render_template("error.html", title="403", message="403 - Forbidden"), 403

@app.errorhandler(404)
def handle_not_found(e):
    return render_template("error.html", title="404", message="404 - Not Found"), 404

@app.errorhandler(405)
def handle_method_not_allowed(e):
    return render_template("error.html", title="405", message="405 - Method Not Allowed"), 405

@app.errorhandler(500)
def handle_internal_error(e):
    return render_template("error.html", title="500", message="500 - Internal Server Error"), 500


#
# Main
#

def main():    
    app.run(host="0.0.0.0", port=80, debug=False)


if __name__ == "__main__":
    main()
