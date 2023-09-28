from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class User(db.Model):
    user_id =db.Column(db.Integer, autoincrement=True,primary_key=True)
    user_username =db.Column(db.String(100),nullable=False)
    user_email =db.Column(db.String(120)) 
    user_pwd=db.Column(db.String(120),nullable=False)
    user_dob=db.Column(db.String(20),nullable=False) 
    user_height=db.Column(db.Integer,nullable=True)
    user_weight=db.Column(db.Integer,nullable=True)
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
    cyc_sys_id=db.Column(db.Integer(),db.ForeignKey("symptomstracking.symptom_id"),nullable=False)
    start_date=db.Column(db.Date(), nullable=False)
    end_date=db.Column(db.Date(), nullable=False)
    cycle_length=db.Column(db.Integer,nullable=False)
    period_length=db.Column(db.Integer,nullable=False)
    note=db.Column(db.Text())
    created_at=db.Column(db.DateTime(), default=datetime.utcnow)
    cycdeets=db.relationship('User',back_populates='cycdeets')
    cycsym=db.relationship('SymptomsTracking',back_populates='cycsym')
    cycmood=db.relationship('MoodTable',back_populates='cycmood',cascade='all,delete-orphan')
    cycovul=db.relationship('Ovulation',back_populates='cycovul',cascade='all,delete-orphan')


class SymptomsTracking(db.Model):
    symptom_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    symptom_type=db.Column(db.String(70),nullable=False)
    Severity=db.Column(db.Integer(),nullable=True)
    recorded_at=db.Column(db.DateTime(),default=datetime.utcnow)
    sys_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False) 
    sypdeets=db.relationship('User',back_populates='sypdeets')
    cycent=db.relationship('CycleEntry',back_populates='cycent',cascade='all,delete-orphan')
    symmed=db.relationship('Medication',back_populates='symmed',cascade='all,delete-orphan')


class MoodTable(db.Model):
    mood_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    mood_entry_id=db.Column(db.Integer(),db.ForeignKey("cycleentry.entry_id"),nullable=False)
    date_recorded=db.Column(db.DateTime(), default=datetime.utcnow)
    mood_swing=db.Column(db.Integer())
    mood_name=db.Column(db.String(100))
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    track_id=db.Column(db.Integer,)
    mooddeets=db.relationship('User',back_populates='mooddeets')
    moodent=db.relationship('CycleEntry',back_populates='moodent')


class Ovulation(db.Model):
    ovulation_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    end_date=db.Column(db.DateTime(), default=datetime.utcnow)
    ovul_entry_id=db.Column(db.Integer,db.ForeignKey("cycleentry.entry_id"),nullable=False)
    ovuldeets=db.relationship('User',back_populates='ovuldeets')
    ovulent=db.relationship('CycleEntry',back_populates='ovulent') 


class Medication(db.Model):
    med_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    symptom_id=db.Column(db.Integer(),db.ForeignKey("symptomstracking.symptom_id"),nullable=False)
    med_name=db.Column(db.String(50))
    dosage=db.Column(db.String(50))
    taken_at=db.Column(db.DateTime(),default=datetime.utcnow)
    medication=db.Column(db.String(100))
    med_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    meddeets=db.relationship('User',back_populates='meddeets')
    medsym=db.relationship('symptomsTracking',back_populates='medsym')


class FamilyPlanning(db.Model):
    familyplan_id=db.Column(db.Integer(),autoincrement=True,primary_key=True)
    fam_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)
    planning_type=db.Column(db.String(255),nullable=False)
    start_date=db.Column(db.DateTime(), default=datetime.utcnow)
    end_date=db.Column(db.DateTime(), default=datetime.utcnow)
    plandeets=db.relationship('User',back_populates='plandeets')


class Admin(db.Model):
    admin_id=db.Column(db.Integer(), autoincrement=True,primary_key=True)
    admin_username=db.Column(db.String(80),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)
    