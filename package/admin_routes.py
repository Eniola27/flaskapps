from flask import render_template,abort

from package import app
from package.models import db
from package.forms import *

@app.route("/admin/")
def admin_login():
    return render_template("admin/login.html")