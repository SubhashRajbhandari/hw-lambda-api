import os
import logging
from dotenv import load_dotenv
from app import create_app, db

# Configure logging for local development
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file for local development
logger.info("Loading environment variables from .env file")
load_dotenv()

# Set environment variable defaults for local development if not in .env
os.environ.setdefault('DB_USERNAME', 'postgresAdmin')
os.environ.setdefault('DB_PASSWORD', 'password')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('DB_NAME', 'hataimaWaiterDB')

# Log database connection (hiding password)
db_uri = f"postgresql://{os.environ.get('DB_USERNAME')}:******@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
logger.info(f"Connecting to database: {db_uri}")

# Create the app
app = create_app()

# Create database tables
try:
    with app.app_context():
        logger.info("Creating database tables if they don't exist")
        db.create_all()
        logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}", exc_info=True)

if __name__ == '__main__':
    logger.info("Starting Flask development server")
    app.run(debug=True)
