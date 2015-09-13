"""
The flask application package.
"""
from Gatekeeper import gatekeeper_config
from flask import Flask
from os import environ

app = Flask(__name__)

app.config.from_object(
    gatekeeper_config.config_dict[environ.get('CONFIG_MODE', 'DEFAULT')])

import Gatekeeper.model.animal
import Gatekeeper.views
