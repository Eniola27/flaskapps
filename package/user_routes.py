from flask import render_template,abort,redirect,flash,make_response,url_for,session,request

from werkzeug.security import generate_password_hash,check_password_hash 
#localimports
from package import app,csrf
from package.models import db,User
from package.forms import *


@app.route("/home")
def home():
    #abort (403)
    return render_template("users/index.html")

@app.route("/login/",methods=['POST','GET'])
def login():
    #abort (403)
    regform=RegForm()
    if request.method=='GET':
        return render_template("users/login.html")
    else:
        username=request.form.get('username')
        pwd=request.form.get('pwd')
        deets=db.session.query(User).filter(User.user_username==username).first()
        if deets != None:
            hashed_pwd=deets.user_pwd
            if check_password_hash(hashed_pwd,pwd)==True:
                session['userloggedin']=deets.user_id
                return redirect("/dashboard")
            else:
                flash("Invalid login,try again")
                return redirect("/login/")

@app.route("/register")
def register():
    #abort (403)
    regform=RegForm()
    if request.method=='GET':
        return render_template("users/register.html",regform=regform)
    else:
        if regform.validate_on_submit():
            username=regform.username.data
            email=regform.email.data
            pwd=regform.pwd.data
            hashed_pwd=generate_password_hash(pwd)
            u=User(user_username=username,user_email=email,user_pwd=hashed_pwd)
            db.session.add(u)
            db.session.commit()
            flash ("Your account has been created. Please Login")
            return redirect('/login/')
        else:
            return render_template("user/register.html",regform=regform)



@app.route("/logout")
def logout():
     if session.get('userloggedin')!=None:
        session.pop('userloggdin',None)
        return redirect("/home")

@app.route("/about/")
def about_page():
    return render_template("users/about.html")                    

@app.route("/dashboard")
def dashboard():
    # if session.get('user') !=None:
    #     return render_template("users/dashboard.html")
    # else:
    #     flash("You must be logged in to view this page") 
        return render_template('users/dashboard.html') 

@app.route("/profile")
def profile():
    return render_template("users/profile.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template ("users/error.html",error=error),404

@app.errorhandler(403)
def page_forbidden(error):
    return render_template ("users/errors.html",error=error),403

