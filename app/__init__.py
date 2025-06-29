import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize SQLAlchemy
db = SQLAlchemy()

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Initialize the Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Configure SQLAlchemy with Aurora DB connection
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.environ.get('DB_USERNAME')}:"
        f"{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:"
        f"{os.environ.get('DB_PORT')}/"
        f"{os.environ.get('DB_NAME')}"
    )
    
    # Log the database URI (with password masked)
    db_uri = app.config['SQLALCHEMY_DATABASE_URI'].replace(
        os.environ.get('DB_PASSWORD', ''), '******')
    logger.info(f"Database URI: {db_uri}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import and register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.waiter_routes import waiter_bp
    from app.routes.menu_routes import menu_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(waiter_bp)
    app.register_blueprint(menu_bp)
    
    logger.info("Flask application initialized with all routes registered")
    return app
