# backend/app/routes/map.py

from flask import Blueprint, render_template

map_bp = Blueprint('map', __name__)

@map_bp.route('/map')
def show_map():
    return render_template('map.html') 