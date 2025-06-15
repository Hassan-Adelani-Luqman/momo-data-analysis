import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS # Import CORS for cross-origin requests
from src.models.user import db # Import the shared db instance
from src.models.sms import Message, Sender, Recipient # Import our new SMS models
from src.routes.user import user_bp
from src.routes.sms import sms_bp # We will create this later for API endpoints
from src.data_processor import parse_xml_and_populate_db # Import our data processing function

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5000",  # Development
            "http://127.0.0.1:5000",  # Development
            "https://your-production-domain.com"  # Production - Replace with your domain
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(sms_bp, url_prefix='/api/v1')

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppresses a warning
db.init_app(app) # Initialize SQLAlchemy with our Flask app

@app.route('/', defaults={'path': ''}) # Route for serving static files (frontend)
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

def initialize_database():
    """Initialize database and load data if needed"""
    with app.app_context(): # This ensures we are within the Flask application context
        db.create_all() # Creates all tables defined by our models (Sender, Recipient, Message)
        
        # Check if data already exists in the Message table
        message_count = Message.query.count()
        if message_count == 0:
            print("No data found. Loading SMS data from XML...")
            # Construct the absolute path to your XML file
            xml_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modified_sms_v2.xml')
            if os.path.exists(xml_file_path):
                parse_xml_and_populate_db(xml_file_path) # Call our data processing function
                print("Data loading completed.")
            else:
                print(f"XML file not found at {xml_file_path}")
        else:
            print(f"Database already contains {message_count} messages.")

if __name__ == '__main__':
    initialize_database() # Call the database initialization function when the script runs
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Determine if we're in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        # Production settings
        app.run(host='0.0.0.0', port=port)
    else:
        # Development settings
        app.run(host='0.0.0.0', port=port, debug=True)