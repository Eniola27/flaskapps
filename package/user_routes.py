from flask import render_template,abort,redirect,flash,make_response,url_for,session,request
from werkzeug.security import generate_password_hash,check_password_hash 
#localimports
from package import app,csrf
from package.models import *
from package.forms import *


@app.route("/home")
def home():
    #abort (403)
    return render_template("users/index.html")

@app.route("/login/",methods=['POST','GET'])
def login():
    #abort (403)
    if request.method=='GET':
        return render_template("users/login.html")
    else:
        username=request.form.get('username')
        pwd=request.form.get('password')
        deets=db.session.query(User).filter(User.user_username==username).first()
        if deets != None:
            hashed_pwd=deets.user_pwd
            if check_password_hash(hashed_pwd,pwd):
                session['userloggedin'] =deets.user_id
                return redirect("/dashboard")
            else:
                flash("Invalid login,try again")
                return redirect("/login/")
        else:
            flash("Invalid login,try again")
            return redirect("/login/")

@app.route("/register",methods=['POST','GET'])
def register():
    #abort (403)
    if request.method=='GET':
        return render_template("users/register.html")
    else:
        email=request.form.get('email')
        username=request.form.get('username')
        pwd=request.form.get('password')
        dob=request.form.get('dob')
        wth=request.form.get('weight')
        hgt=request.form.get('height')
        hashed_pwd=generate_password_hash(pwd)
        u=User(user_username=username,user_email=email,user_pwd=hashed_pwd,user_dob=dob,user_weight=wth,user_height=hgt)
        db.session.add(u)
        db.session.commit()
        flash ("Your account has been created. Please Login")
        return redirect('/login/')
    
        return render_template("user/register.html")



@app.route("/logout")
def logout():
     if session.get('userloggedin')!=None:
        session.pop('userloggedin',None)
        return redirect("/home")

@app.route("/about/")
def about_page():
    return render_template("users/about.html")                    

@app.route("/dashboard")
def dashboard():
    if session.get('userloggedin') ==None:
        flash("You must be logged in to view this page")
        return render_template("users/login.html")
    else:
        userid=session.get('userloggedin')
        user=db.session.query(User).filter(User.user_id==userid).first()
        return render_template('users/dashboard.html',user=user) 

@app.route("/profile",methods=['POST','GET'])
def profile():
    userid=session.get('userloggedin')
    user=db.session.query(User).filter(User.user_id==userid).first()
    cycle=db.session.query(CycleEntry).filter(CycleEntry.cyc_user_id==userid).first()
    return render_template("users/profile.html",cycle=cycle,userid=userid,user=user)


@app.route("/editprofile/<id>",methods=['post','get'])
def edit_profile(id):
    if request.method =='GET':
        deets=db.session.query(CycleEntry).filter(CycleEntry.entry_id==id).first_or_404()
        return render_template("users/edit_cycle_profile.html",deets=deets)
    else:
        cycle_2update =CycleEntry.query.get(id)
        cycle_2update.cycle_length=request.form.get('cycleLength')
        cycle_2update.period_length=request.form.get('periodLength')
        cycle_2update.lastperioddate=request.form.get('lastPeriod')
        cycle_2update.note=request.form.get('note')
        # c=CycleEntry(cyc_user_id=id, cycle_length=cycle,period_length=period,lastperioddate=last,note=note)
        # db.session.add(c)
        db.session.commit()
        flash('cycle was updated',category='success')
        return redirect(url_for('profile'))

@app.route("/edituser/<id>",methods=['post','get'])
def edit_user(id):
    if request.method =='GET':
        deets=db.session.query(User).filter(User.user_id==id).first_or_404()
        return render_template("users/edit_profile.html",deets=deets)
    else:
        user_2update =User.query.get(id)
        user_2update.user_email=request.form.get('email')
        user_2update.user_dob=request.form.get('dob')
        user_2update.user_weight=request.form.get('weight')
        user_2update.user_height=request.form.get('height')
        # c=CycleEntry(cyc_user_id=id, cycle_length=cycle,period_length=period,lastperioddate=last,note=note)
        # db.session.add(c)
        db.session.commit()
        flash('cycle was updated',category='success')
        return redirect(url_for('profile'))

@app.route("/calculator")
def calculator():
    return render_template("users/calculator.html")


@app.route("/calendar")
def calendar():
    return render_template("users/calendar.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template ("users/error.html",error=error),404

@app.errorhandler(403)
def page_forbidden(error):
    return render_template ("users/errors.html",error=error),403

