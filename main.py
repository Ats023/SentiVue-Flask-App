from flask import Flask
from website import create_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from dash_app.main import dash_app as my_dash_app
#only run the app when the main file is run directly
app = create_app()
migrate = Migrate(app, app.db)
#my_dash_app.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)