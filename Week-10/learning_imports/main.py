"""
File structure
main.py
flaskr
    controller
        app.py
            app()
    __init__.py
        create_app()
    db.py
        init_db()
"""


# The sub folders also become a module
from flaskr.controller.app import app
app()


import flaskr as f
f.create_app()


from flaskr.db import init_db
init_db()