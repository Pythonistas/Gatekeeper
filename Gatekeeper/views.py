"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Gatekeeper import app


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/dogs')
def dog_summary():
    """Renders the static dog summary page."""
    return render_template(
        'dog_summary.html',
        title='Dogs',
        year=datetime.now().year,
        message='Your dog summary page.',
        static_string='I\'ve got a bad feeling about this...',
        dogs=[0,1,2,3,4,5,6,7]
    )
