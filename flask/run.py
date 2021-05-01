# -*- coding: utf-8 -*-
# flask/run.py
# точка входа
from app import create_app

app = create_app()


# точка входа
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
