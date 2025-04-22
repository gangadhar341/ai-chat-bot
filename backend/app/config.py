import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../', '.env'))

class Config:
   
    # CORS Config
    CORS_RESOURCES = {r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"]}}
    CORS_HEADERS = 'Content-Type, Authorization, X-Requested-With, Accept'
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = 'Authorization, Content-Type'
    CORS_MAX_AGE = 86400

