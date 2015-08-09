"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify
from Gatekeeper import app
from Gatekeeper.model import animal


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/api/dogs')
def dogs():
    """Renders a list of dogs"""
    all_dogs = animal.load_from_yaml()
    return jsonify(dogs=[cur_dog.to_json_dict('name', 'age', 'breed') for cur_dog in all_dogs])
    #return jsonify(dogs=[cur_dog.to_json_dict() for cur_dog in all_dogs])

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
