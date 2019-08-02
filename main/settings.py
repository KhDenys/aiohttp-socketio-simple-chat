import os

from pathlib import Path

from dotenv import load_dotenv


PROJECT_PATH = Path.cwd()
STATIC_PATH = str(PROJECT_PATH / 'static')
TEMPLATES_PATH = str(PROJECT_PATH / 'templates')
MESSAGE_COLLECTION = 'messages'
USER_COLLECTION = 'users'


load_dotenv(dotenv_path=PROJECT_PATH)


config = {
    'DEBUG': os.getenv('DEBUG'),
    'HOST': os.getenv('HOST'),
    'PORT': os.getenv('PORT'),
    'PROJECT_PATH': str(PROJECT_PATH),
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'mongodb_config': {
        'HOST': os.getenv('MONGODB_HOST'),
        'DB_NAME': os.getenv('MONGODB_DB_NAME'),
    }
}
