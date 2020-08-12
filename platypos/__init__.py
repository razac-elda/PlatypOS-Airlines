from flask import Flask

app = Flask(__name__)

from platypos import routes
