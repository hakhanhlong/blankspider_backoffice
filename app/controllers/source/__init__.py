from flask import Blueprint
source = Blueprint('source', __name__)

from . import views