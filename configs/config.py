app_config = {
    "host":"0.0.0.0",
    "port":"5050"
}

dbconfig = {
    "host":"127.0.0.1",
    "port":"3306",
    "username":"root",
    "password":"",
    "database":"countract_db"
}

key_jwt = {
    "key":"kumakumabear"
}

import os

# Set environment variables
os.environ['app_host'] = '0.0.0.0'
os.environ['app_port'] = '5000'

os.environ['db_host'] = 'host.docker.internal'
os.environ['db_port'] = '3306'
os.environ['db_username'] = 'jinfra22'
os.environ['db_password'] = 'redgemastikaye'
os.environ['db_database'] = 'countract_db'

os.environ['key_jwt'] = 'kumakumabear'