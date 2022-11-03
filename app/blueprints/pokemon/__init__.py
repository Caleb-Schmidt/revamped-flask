from flask import Blueprint

bp = Blueprint('pokemon', __name__, url_prefix='/pokemon')

from . import routes