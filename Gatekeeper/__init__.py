"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

app.config['ERROR_404_HELP'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

import Gatekeeper.views
import Gatekeeper.model.animal
