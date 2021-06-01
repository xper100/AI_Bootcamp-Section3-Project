from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

db = SQLAlchemy()
migrate = Migrate()

DATABASE_URI = "postgresql+psycopg2://postgres:Wndbs9526!@localhost:5432/hospital"

engine = create_engine(DATABASE_URI)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Wndbs9526!@localhost:5432/hospital"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config is not None:
        app.config.update(config)
 


    db.init_app(app)
    migrate.init_app(app, db)

    from hospital_app.routes import (main_route, search_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(search_route.bp, url_prefix='/api')

    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
