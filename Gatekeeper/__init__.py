"""
The flask application package.
"""
import logging

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from os import environ
from pymongo import *

from Gatekeeper import gatekeeper_config

app = Flask(__name__)

app.config.from_object(
    gatekeeper_config.config_dict[environ.get('CONFIG_MODE', 'DEBUG')])

# Configure Mongo database connection
try:
    app.config['MONGO_CONNECTION'] = MongoClient('localhost', 27017)
    app.config['GATEKEEPERDB'] = app.config['MONGO_CONNECTION']['Gatekeeper']
except errors.ConnectionFailure:
    print("Connection failed")

# Refresh the log level setting - if we don't do this, the
# DebugToolbarExtension won't catch any messages.
logging.getLogger().setLevel(logging.DEBUG if app.debug else logging.INFO)

toolbar = DebugToolbarExtension(app)

import Gatekeeper.model.animal
import Gatekeeper.views
