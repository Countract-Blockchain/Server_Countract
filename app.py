from flask import Flask
import os
from configs.config import app_config

app = Flask(__name__, static_folder=None)
config = {}
config['app_host'] = os.getenv('app_host')
config['app_port'] = os.getenv('app_port')

if config['app_host'] == None:
    config['app_host'] = app_config['host']

if config['app_port'] == None:
    config['app_port'] = app_config['port']

try:
    from controllers.user_controller import *
    from controllers.dokumen_controller import *
    from controllers.akses_controller import *
except Exception as e:
    print(e)


if __name__ == '__main__':
    # print("Server is running on host: " + config['app_host'] + " and port: " + config['app_port'])
    @app.route("/")
    def index():
        return "This is Countract"
    app.run(debug=True, host='0.0.0.0', port='5000')