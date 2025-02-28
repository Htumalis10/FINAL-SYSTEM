import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    
    # MySQL database configuration for PythonAnywhere
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'Htumalis10.mysql.pythonanywhere-services.com')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'Htumalis10')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')  # You'll set this in PythonAnywhere
    MYSQL_DB = os.environ.get('MYSQL_DB', 'Htumalis10$thriftstore')
    
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 