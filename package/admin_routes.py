from flask import render_template,abort,request,redirect,flash,url_for,session

from package import app
from package.models import db,Admin
from package.forms import *

@app.route("/admin")
def admin_page():
    if session.get('adminuser')==None or session.get('role')!='admin':
        return render_template("admin/login.html")
    else:
        return redirect(url_for('admin_dashboard'))
    

@app.route('/admin/login/',methods=['POST','GET'])
def admn_login():
    if request.method=='GET':
        return render_template('admin/login.html')
    else:
        username=request.form.get('username')
        pwd=request.form.get('pwd')
        check=db.session.query(Admin).filter(Admin.admin_username==username,Admin.admin_pwd==pwd).first()
        if check:
            session['adminuser']=check.admin_id
            session['role']='admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid Login',category='warning')
            return redirect(url_for('admin_login'))
        

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('adminuser')==None or session.get('role')!='admin':
        return redirect(url_for('admin_login'))
    else:
        return render_template('admin/dashboard.html')
    

@app.route('/admin/logout')
def admin_logout():
    if session.get('adminuser')!=None:
        session.pop('adminuser',None)
        session.pop('role',None)
        flash('You are logged out',category='info')
        return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))