"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import Gatekeeper.views
import Gatekeeper.model.animal
