# SQL model for JSON conversion
from dataclasses import dataclass
from config import db
from datetime import datetime

# for Comment table
@dataclass
class Comment(db.Model):
    __tablename__ = "Comment"
    __table_args__ = {'schema': 'CW2'}

    Comment_ID = db.Column(db.Integer, primary_key=True)
    Trail_ID = db.Column (db.Integer, db.ForeignKey("CW2.Trail.Trail_ID"), nullable=False)
    User_ID = db.Column(db.Integer, db.ForeignKey("CW2.User.User_ID"), nullable=False)
    Content = db.Column(db.String(500)) #nullable=True?
    CreatedOn =db.Column(db.DateTime, default=datetime.utcnow)
    IsArchived = db.Column(db.Boolean, default=False)

# for user table (for the roles)
class User(db.Model):
    __tablename__ = "User"
    __table_args__ = {'schema': 'CW2'}
    User_ID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True)
    Role = db.Column(db.String(5), nullable=False)

# for trail table (maybe read-only?)
class Trail(db.Model):
    __tablename__ = "Trail"
    __table_args__ = {'schema': 'CW2'}

    Trail_ID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(255), nullable=False)
    Rating = db.Column(db.Numeric(2,1))
    Difficulty = db.Column(db.String(10))
    Location = db.Column(db.String(255), nullable=False)
    EstimatedTime = db.Column(db.String(20))
    Distance = db.Column(db.Numeric(5,1))
    ElevationGain = db.Column(db.Integer)
    TrailType = db.Column(db.String(15))
    Description = db.Column(db.String(500))