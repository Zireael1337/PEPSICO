# -*- coding: utf-8 -*-
# app/config.py
# конфиг
from app.extensions import ServiceDB


class BaseConfig(object):
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = ServiceDB.gen_key()
    SQLALCHEMY_DATABASE_URI = ServiceDB.get_path_url(__file__, "sap.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProductionConfig(BaseConfig):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
