from flask import Flask
import os
# from configs.config import app_config

app = Flask(__name__, static_folder=None)
config = {}
config['host'] = os.getenv('app_host')
config['port'] = os.getenv('app_port')

# if config['host'] == None:
#     config['host'] = app_config['host']

# if config['port'] == None:
#     config['port'] = app_config['port']

try:
    from controllers.user_controller import *
    from controllers.dokumen_controller import *
    from controllers.akses_controller import *
except Exception as e:
    print(e)

# @app.route("/")
# def index():
#     return "This is Countract"

if __name__ == '__main__':
    app.run(debug=True, host=config['host'], port=config['port'])