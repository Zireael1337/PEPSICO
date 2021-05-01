# -*- coding: utf-8 -*-
from flask import Flask
from .extensions import db
from .main import main


def create_app():
    # создание экземпляра приложения
    app = Flask(__name__)
    # применение конфигурации
    #app.config.from_object('config.ProductionConfig')
    app.config.from_object('config.DevelopmentConfig')
    # импорт своих модулей (blueprint)
    app.register_blueprint(main)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    if app.debug is True:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)
        except ImportError:
            pass

    return app
