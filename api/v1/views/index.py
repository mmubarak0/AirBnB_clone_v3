#!/usr/bin/python3
"""
set up route for status endpoint
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """ send status api"""
    return {"status": "OK"}


@app_views.app_errorhandler(404)
def handle_404(err):
    """Handle 404 page not found error."""
    return jsonify({"error": "Not found"})
