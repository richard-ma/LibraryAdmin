import os

PROJECT_ROOT = os.path.dirname(__file__)
DATABASE = os.path.join(PROJECT_ROOT, "data", "libraryadmin.db")
SECRET_KEY = "development key"
DEBUG = True
