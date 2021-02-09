from flask import Flask #memanggil librari falsk
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes