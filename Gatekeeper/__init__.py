"""
The flask application package.
"""
from os import environ

from flask import Flask

from Gatekeeper import gatekeeper_config

app = Flask(__name__)

app.config.from_object(gatekeeper_config.config_dict[environ.get('CONFIG_MODE', 'DEFAULT')])

import Gatekeeper.views
import Gatekeeper.model.animal
