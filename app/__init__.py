from flask import Flask

app = Flask(__name__)

from app.main.index import main as main
from app.main.index import result as result
from app.main.index import metabase as metabase

app.register_blueprint(main)
app.register_blueprint(result)
app.register_blueprint(metabase)