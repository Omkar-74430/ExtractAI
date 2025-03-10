from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from web_scraper import process_results

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Ensure 'temp' directory exists for temporary files
if not os.path.exists('temp'):
    os.makedirs('temp')

# Home Route - Serves Frontend
@app.route('/')
def home():
    return render_template('index.html')

# Search API - Handles Queries and Returns Processed Results
@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        logging.info(f"Received query: {query}")

        # Process the query using the web scraper
        search_results = process_results(query)

        # Check if results are empty
        if not search_results:
            return jsonify({
                "error": "No relevant results found",
                "query": query,
                "best_url": "",
                "headlines": [],
                "contents": []
            })

        # Return formatted response
        return jsonify({
            "query": query,
            "best_url": search_results.get('best_url', ''),
            "headlines": search_results.get('headlines', []),
            "contents": search_results.get('contents', [])
        })

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
