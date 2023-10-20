"""[General Configuration Params]
"""
from os import environ, path
import os
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

APP_TITLE = os.environ.get('APP_TITLE')
GENHEALTH_API_KEY = os.environ.get('GENHEALTH_API_KEY')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')