import os
from app import create_app  # Import after loading environment variables


app = create_app()


if __name__ == '__main__':
    with app.app_context():

        app.config['FLASK_ENV'] = 'development'

        # Create all tables and seed data
        #db.create_all()  # Create all tables
        app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", 5001))
