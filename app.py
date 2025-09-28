from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')

from routes import *

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)