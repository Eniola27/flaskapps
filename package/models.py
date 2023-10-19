from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class User(db.Model):
    user_id =db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_username =db.Column(db.String(100),nullable=False)
    user_email =db.Column(db.String(120)) 
    user_pwd=db.Column(db.String(120),nullable=False)
    user_dob=db.Column(db.Date(),nullable=False) 
    user_height=db.Column(db.Integer,nullable=True)
    user_weight=db.Column(db.Integer,nullable=True)
    user_pix=db.Column(db.String(120),nullable=True) 
    user_datejoined=db.Column(db.DateTime(), default=datetime.utcnow)#default
    #relationships
    userdeets=db.relationship('CycleEntry',back_populates='cycdeets',cascade='all, delete-orphan')
    usersyp=db.relationship('SymptomsTracking',back_populates='sypdeets',cascade='all, delete-orphan')
    usermood=db.relationship('MoodTable',back_populates='mooddeets',cascade='all, delete-orphan')
    userovul=db.relationship('Ovulation',back_populates='ovuldeets',cascade='all, delete-orphan')
    usermed=db.relationship('Medication',back_populates='meddeets',cascade='all, delete-orphan')
    userplan=db.relationship('FamilyPlanning',back_populates='plandeets',cascade='all, delete-orphan')
    

class CycleEntry(db.Model):
    entry_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    cyc_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    cycle_length=db.Column(db.Integer,nullable=False,default=7,server_default="7")
    period_length=db.Column(db.Integer,nullable=False,default=28, server_default="28")
    lastperioddate=db.Column(db.Date(),nullable=False)
    note=db.Column(db.Text())
    created_at=db.Column(db.DateTime(), default=datetime.utcnow)
    cycdeets=db.relationship('User',back_populates='userdeets')
    cycmood=db.relationship('MoodTable',back_populates='moodcyc',cascade='all,delete-orphan')
    cycovul=db.relationship('Ovulation',back_populates='ovulcyc',cascade='all,delete-orphan')


class SymptomsTracking(db.Model):
    symptom_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    symptom_type=db.Column(db.String(70),nullable=True)
    Severity=db.Column(db.Integer(),nullable=True)
    recorded_at=db.Column(db.Date())
    sys_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False) 
    sypdeets=db.relationship('User',back_populates='usersyp')
    symmed=db.relationship('Medication',back_populates='medsym',cascade='all,delete-orphan')
    sypmood=db.relationship('MoodTable',back_populates='moodsyp',cascade='all,delete-orphan')


class MoodTable(db.Model):
    mood_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    mood_entry_id=db.Column(db.Integer(),db.ForeignKey("cycle_entry.entry_id"),nullable=False)
    date_recorded=db.Column(db.Date())
    mood_swing=db.Column(db.Enum('1','0'))
    mood_name=db.Column(db.String(100))
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    symptom_id=db.Column(db.Integer(),db.ForeignKey("symptoms_tracking.symptom_id"),nullable=False)
    mooddeets=db.relationship('User',back_populates='usermood')
    moodcyc=db.relationship('CycleEntry',back_populates='cycmood')
    moodsyp=db.relationship('SymptomsTracking',back_populates='sypmood')


class Ovulation(db.Model):
    ovulation_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    end_date=db.Column(db.DateTime(), default=datetime.utcnow)
    ovul_entry_id=db.Column(db.Integer,db.ForeignKey("cycle_entry.entry_id"),nullable=False)
    ovuldeets=db.relationship('User',back_populates='userovul')
    ovulcyc=db.relationship('CycleEntry',back_populates='cycovul')


class Medication(db.Model):
    med_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    symptom_id=db.Column(db.Integer(),db.ForeignKey("symptoms_tracking.symptom_id"),nullable=False)
    med_name=db.Column(db.String(50))
    dosage=db.Column(db.String(50))
    taken_at=db.Column(db.Date())
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    meddeets=db.relationship('User',back_populates='usermed')
    medsym=db.relationship('SymptomsTracking',back_populates='symmed')


class FamilyPlanning(db.Model):
    familyplan_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    planning_type=db.Column(db.String(255),nullable=False)
    start_date=db.Column(db.Date())
    end_date=db.Column(db.Date())
    plandeets=db.relationship('User',back_populates='userplan')


class Admin(db.Model):
    admin_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(80),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)
    