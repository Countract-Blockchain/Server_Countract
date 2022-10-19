from flask import Flask
from configs.config import app_config

app = Flask(__name__, static_folder=None)
# from controllers.dokumen_controller import *
# from controllers.user_controller import *
# from controllers.dokumen_controller import *

try:
    from controllers.user_controller import *
    from controllers.dokumen_controller import *
    from controllers.akses_controller import *
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(debug=True, host=app_config['host'], port=app_config['port'])