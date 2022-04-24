from flask import Flask

app=None

def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static')
    app.config['SECRET_KEY'] = 'cbsrbvkrsvrs31sr13r5svsr1vc3r5srs35rsr3vc5sv35r1ssv135v'
    app.app_context().push()
    return  app

app= create_app()
from application.controllers import *


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)