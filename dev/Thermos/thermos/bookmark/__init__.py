from flask import Blueprint

auth = Blueprint('bookmark', __name__)

from . import views