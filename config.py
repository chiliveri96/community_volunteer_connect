# config.py
import os

class Config:
    SECRET_KEY = os.urandom(24)  # Used for sessions and flash messages
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Akhil369@localhost/community_connect'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
