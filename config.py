import os


BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)

SECRET_KEY = 'dev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pyboard.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
