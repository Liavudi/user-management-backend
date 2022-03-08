import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DBURL = os.getenv('MYAPPDB')
DB = 'myapp'
