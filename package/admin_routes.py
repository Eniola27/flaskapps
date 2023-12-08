from functools import wraps
from flask import render_template,abort,request,redirect,flash,url_for,session

from package import app
from package.models import db,Admin,User,FamilyPlanning
from package.forms import *




@app.route("/admin")
def admin_page():
    if session.get('adminuser')==None or session.get('role')!='admin':
        return render_template("admin/login.html")
    else:
        return redirect(url_for('admin_dashboard'))
    

@app.route('/admin/login/',methods=['POST','GET'])
def admin_login():
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
    
@app.route('/familyplanning')
def fam_plan():
    fam=db.session.query(FamilyPlanning).all()
    return render_template("admin/familyplanning.html",fam=fam)

    
@app.route('/allusers')

def all_users():
    user=db.session.query(User).all()
    return render_template("admin/allusers.html",user=user)
