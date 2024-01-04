import os

class Config:
    SECRET_KEY = '29122003'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use a proper database in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
