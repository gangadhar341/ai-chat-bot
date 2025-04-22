import os
from dotenv import load_dotenv
from logging.config import dictConfig
from flask import Flask, Blueprint, jsonify, request
from app.config import Config
from app.rag_service import RAGService
from flask_cors import CORS
from flask import current_app as app



def create_app():
# Load environment variables from .env file
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '../', '.env'))
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    }) 
    


    app = Flask(__name__)
    rag_blueprint = Blueprint('rag_blueprint', __name__)

    app.config.from_object(Config)


    app.logger.info('app created')

    CORS(app, resources={
        r"/api*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"]
        }
    })

    @rag_blueprint.route("/", methods=["POST", "OPTIONS"])
    def ask_gpt():
        """Post request for GPT"""
        try:
            if request.method == "OPTIONS":
                return jsonify({"status": "OK"}), 200
            data = request.get_json()
            app.logger.info(f"Received data: {data}")
            result = RAGService.ask_gpt(data)
            return jsonify({"message": f"Result is ${result}"}), 200
        except Exception as e:
            app.logger.error(f"Error Processing Document: {e}", exc_info=True)

            # Default to internal server error
            status_code = 500
            error_message = str(e)

            # Handle specific quota-exceeded error
            if "insufficient_quota" in error_message or "429" in error_message:
                status_code = 429
                error_message = "You have exceeded your OpenAI API quota. Please check your plan and billing details."

            return jsonify({"error": error_message}), status_code

        
    app.register_blueprint(rag_blueprint, url_prefix='/api') 
    return app