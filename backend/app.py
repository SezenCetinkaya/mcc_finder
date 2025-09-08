from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from scraper.scrapling_scraper import fetch_full_page_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Adaptive cache to store URLs that have been scraped
adaptive_cache = {}

@app.route('/scrape', methods=['POST'])
@cross_origin(origin='http://localhost:3000')
def scrape():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL girilmedi"}), 400

    # If URL already exist first_time=False
    first_time = not adaptive_cache.get(url, False)

    dynamic_data = fetch_full_page_data(url, first_time=first_time)

    # URL is aded to cache
    adaptive_cache[url] = True

    return jsonify(dynamic_data)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
