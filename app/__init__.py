from flask import Flask
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = 'pinhamonhangaba'
migrate = Migrate(app)


from app.view import homepage