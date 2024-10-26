import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    XENDIT_PUBLIC_KEY = os.getenv('XENDIT_PUBLIC_KEY')
    XENDIT_SECRET_KEY = os.getenv('XENDIT_SECRET_KEY')