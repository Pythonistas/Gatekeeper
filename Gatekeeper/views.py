"""
Routes and views for the flask application.
"""

from Gatekeeper import app
from datetime import datetime
from flask import render_template


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


@app.route('/dog_summary')
def static_dogs():
    """Renders the dog summary page using client-side templating and static dog data."""
    return render_template(
        'dog_summary.html',
        title='Dogs',
        year=datetime.now().year,
        message='Your dog summary page.',
    )


@app.route('/dogs/new')
def dogs_new():
    """Renders the simplified new dog form."""
    return render_template(
        'dog_form.html',
        title='Dogs',
        year=datetime.now().year,
        message='Your new dog entry form.',
    )
