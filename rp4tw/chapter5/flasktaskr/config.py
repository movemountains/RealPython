import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
DATABASE = 'flasktask.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '02ij3bNN7GHBBWmLuNveRSDfjEVfXRH1d3NkGsQi2FfgtAeiOyshp9VnNgYt3hqS'

# Full path to the database
DATABASE_PATH = os.path.join(basedir, DATABASE)