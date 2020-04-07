import os


class Config:
    """Set Flask configuration vars from .env file."""

    SECRET_KEY = 'randomsecretkey'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True