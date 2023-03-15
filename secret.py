from os import environ

import dotenv

dotenv.load_dotenv('.env')
SECRET_KEY = environ['SECRET_KEY']
