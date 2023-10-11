from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


csrf=CSRFProtect()


def create_app():
    from package.models import db
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile("config.py",silent=True)
    db.init_app(app)
    migrate=Migrate(app,db)
    csrf.init_app(app)
    return (app)

app = create_app()

from package import admin_routes ,user_routes
from package.forms import *