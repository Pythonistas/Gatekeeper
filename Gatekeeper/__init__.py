"""
The flask application package.
"""
from os import environ

from flask import Flask

from Gatekeeper import gatekeeper_config

app = Flask(__name__)

if 'CONFIG_MODE' in environ:
    app.config.from_object(eval(gatekeeper_config.config_dict[environ['CONFIG_MODE']]))
else:
    app.config.from_object(eval(gatekeeper_config.config_dict['DEFAULT']))

import Gatekeeper.views
import Gatekeeper.model.animal
