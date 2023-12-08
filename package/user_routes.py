from functools import wraps
from flask import render_template,abort,redirect,flash,make_response,url_for,session,request
from werkzeug.security import generate_password_hash,check_password_hash 


#localimports
from package import app,csrf
from package.models import *
from package.forms import *


def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get("userloggedin") !=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied")
            return redirect("/login")
    return  login_check


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
                flash("Invalid login,try again",category="error")
                return redirect("/login/")
        else:
            flash("Invalid login,try again",category="error")
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
@login_required
def dashboard():
    if session.get('userloggedin') ==None:
        flash("You must be logged in to view this page")
        return render_template("users/login.html")
    else:
        userid=session.get('userloggedin')
        user=db.session.query(User).filter(User.user_id==userid).first()
        return render_template('users/dashboard.html',user=user) 

@app.route("/profile",methods=['POST','GET'])
@login_required
def profile():
    userid=session.get('userloggedin')
    user=db.session.query(User).filter(User.user_id==userid).first()
    cycle=db.session.query(CycleEntry).filter(CycleEntry.cyc_user_id==userid).first()
    symptoms=db.session.query(SymptomsTracking).filter(SymptomsTracking.sys_user_id==userid).first()
    mood=db.session.query(MoodTable).filter(MoodTable.user_id==userid).first()
    return render_template("users/profile.html",cycle=cycle,userid=userid,user=user,symptoms=symptoms,mood=mood)




@app.route("/addprofile/<id>",methods=['post','get'])
@login_required
def add_profile(id):
    if request.method =='GET':
        deets=db.session.query(CycleEntry).filter(CycleEntry.entry_id==id).first()
        return render_template("users/add_cycle_profile.html",deets=deets)
    else: 
        cycle_length=request.form.get('cycleLength')
        period_length=request.form.get('periodLength')
        lastperioddate=request.form.get('lastPeriod')
        note=request.form.get('note')
        c=CycleEntry(cyc_user_id=id, cycle_length=cycle_length,period_length=period_length,lastperioddate=lastperioddate,note=note)
        symptoms=request.form.get('symptoms')
        numbers=request.form.get('numbers')
        daterecorded=request.form.get('daterecorded')
        mood=request.form.get('mood')
        moodSwing=request.form.get('moodSwing')
        daterecord=request.form.get('daterecord')
        db.session.add(c)
        deets=db.session.query(CycleEntry).filter(CycleEntry.cyc_user_id==id).first()
        s=SymptomsTracking(sys_user_id=id,symptom_type=symptoms,Severity=numbers,recorded_at=daterecorded)
        db.session.add(s)
        sub=db.session.query(SymptomsTracking).filter(SymptomsTracking.sys_user_id==id).first()
        if moodSwing =='Yes':
            m=MoodTable(mood_entry_id=deets.entry_id,mood_name=mood,mood_swing="1",date_recorded=daterecord,user_id=id,symptom_id=sub.symptom_id)
        else:
             m=MoodTable(mood_entry_id=deets.entry_id,mood_name=mood,mood_swing="0",date_recorded=daterecord,user_id=id,symptom_id=sub.symptom_id)
        db.session.add(m)
        db.session.commit()
        flash('cycle was added',category='success')
        return redirect(url_for('profile'))



@app.route("/editprofile/<id>",methods=["POST","GET"])
@login_required
def edit_profile(id):
    deets=db.session.query(CycleEntry).filter(CycleEntry.cyc_user_id==id).first()
    symp=db.session.query(SymptomsTracking).filter(SymptomsTracking.sys_user_id==id).first()
    mood=db.session.query(MoodTable).filter(MoodTable.user_id==id).first()
    if request.method =='GET':
        
        return render_template("users/edit_cycle_profile.html",deets=deets,symp=symp,mood=mood)
    else:
        cycle_2_update=CycleEntry.query.get(deets.entry_id)
        symptom_2_update=SymptomsTracking.query.get(symp.symptom_id)
        mood_2_update=MoodTable.query.get(mood.mood_id)
        cycle_2_update.cycle_length=request.form.get('cycleLength')
        cycle_2_update.period_length=request.form.get('periodLength')
        cycle_2_update.lastperioddate=request.form.get('lastPeriod')
        cycle_2_update.note=request.form.get('note')
        symptom_2_update.symptom_type=request.form.get('symptoms')
        symptom_2_update.Severity=request.form.get('numbers')
        symptom_2_update.recorded_at=request.form.get('daterecorded')
        mood_2_update.mood_name=request.form.get('mood')
        moodSwing=request.form.get('moodSwing')
        if moodSwing =='Yes':
            newmood='1'
        else:
            newmood='0'
        mood_2_update.mood_swing=newmood
        mood_2_update.date_recorded=request.form.get('daterecord')
        db.session.commit()
        flash('cycle was updated',category='success')
        return redirect(url_for('profile'))


@app.route("/edituser/<id>",methods=['post','get'])
@login_required
def edit_user(id):
    deets=db.session.query(User).filter(User.user_id==id).first_or_404()
    if request.method =='GET':
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
        flash('information was updated',category='success')
        return redirect(url_for('profile'))
    

@app.route("/changedp/",methods=['GET','POST'])
def changedp():
    id=session.get('userloggedin')
    userdeets =db.session.query(User).get(id)
    if request.method =="GET":
        return render_template("users/changedp.html",userdeets=userdeets)
    else:
            pix= request.files.get('dp')
            filename=pix.filename #we can rename to avaoid name clash
            pix.save(app.config['USER_PROFILE_PATH']+filename)# this has been defined in config
            userdeets.user_pix= filename
            db.session.commit()
            flash("Profile picture updated")
            return redirect(url_for('dashboard'))
    

@app.route("/symptoms",methods=['GET','POST'])
@login_required
def Symptom():
    return render_template("users/symptoms.html")


@app.route("/mood",methods=['GET','POST'])
@login_required
def Mood():
    return render_template("users/mood.html")

@app.route("/family_planning",methods=['GET','POST'])
@login_required
def family_plan():
    userid=session.get('userloggedin')
    user=db.session.query(User).get(userid)
    famplan=db.session.query(FamilyPlanning).filter(FamilyPlanning.user_id==userid).all()
    return render_template("users/family_plan.html",famplan=famplan,user=user)

@app.route("/add_family_planning/<id>",methods=['GET','POST'])
@login_required
def add_family_planning(id):
    user=db.session.query(User).get(id)
    if request.method =='GET':
        plan=db.session.query(FamilyPlanning).filter(FamilyPlanning.user_id==id).all()
        return render_template("users/add_family_planning.html",plan=plan,user=user)
    else:
        planning_type=request.form.get('planningtype')
        start_date=request.form.get('start_date')
        end_date=request.form.get('end_date')
        f=FamilyPlanning(user_id=id,planning_type=planning_type,start_date=start_date,end_date=end_date)
        db.session.add(f)
        db.session.commit()
        flash('family plan was added',category='success')
        return redirect(url_for('family_plan'))


@app.route("/medication",methods=['POST','GET'])
@login_required
def medications():
    userid=session.get('userloggedin')
    user=db.session.query(User).filter(User.user_id==userid).first()
    med=db.session.query(Medication).filter(Medication.user_id==userid).first()
    return render_template("users/medications.html",user=user,med=med)


@app.route("/addmedication/<id>",methods=['GET','POST'])
@login_required
def add_medication(id):
    meds=db.session.query(Medication).filter(Medication.user_id==id).first()
    symp=db.session.query(SymptomsTracking).filter(SymptomsTracking.sys_user_id==id).first()
    if request.method =='GET':
        return render_template("users/add_medication.html",meds=meds,symp=symp)
    else:
       med_name=request.form.get('medication_name')
       dosage=request.form.get('dosage')
       taken_at=request.form.get('date_taken')
       meed=Medication(symptom_id=symp.symptom_id,med_name=med_name,dosage=dosage,taken_at=taken_at,user_id=session['userloggedin'])
       db.session.add(meed)
       db.session.commit()
       flash('Medication was added',category='success')
       return redirect(url_for('medications'))


@app.route("/calendar")
@login_required
def calendar():
    ovulation=db.session.query(Ovulation).filter(Ovulation.user_id==session['userloggedin']).first()
    return render_template("users/calendar.html", ovulation= ovulation)

@app.errorhandler(404)
def page_not_found(error):
    return render_template ("users/error.html",error=error),404

@app.errorhandler(403)
def page_forbidden(error):
    return render_template ("users/errors.html",error=error),403

