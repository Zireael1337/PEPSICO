# -*- coding: utf-8 -*-
# app/auth/__init__.py

from flask import Blueprint

main = Blueprint('main', __name__, template_folder='templates')

from . import views
