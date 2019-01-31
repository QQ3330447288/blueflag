from flask import Flask

app = Flask(__name__)  # parameter is application's models or package's name;initialize class
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.debug = True
# regist blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint)
