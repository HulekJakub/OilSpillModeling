from os import path

# KEEP ALL SECRETS IN ../config.local.py !!!
SECRET_KEY = "CHANGE_ME"  # does not matter, remember to change it if app is working in the production environment!!!
APP_NAME = "Oil Spill Modeling"
APP_DEBUG = False

LOG_DIR = 'logs'
DEBUG_LOG = path.join(LOG_DIR, 'debug.log')
ERROR_LOG = path.join(LOG_DIR, 'error.log')

