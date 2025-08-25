from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper.static_scraper import get_static_content
from scraper.dynamic_scraper import get_dynamic_content
from scraper.text_processor import extract_meaningful
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL girilmedi"}), 400

    # collecting Static and dynamic data
    static_data = get_static_content(url)
    dynamic_data = get_dynamic_content(url)

    # combining texts for processing
    combined_text = ""
    if "html" in static_data:
        combined_text += static_data["html"] + " "
    if "html" in dynamic_data:
        combined_text += dynamic_data["html"]

    # meaningful text extraction
    soup = BeautifulSoup(combined_text, "html.parser")
    plain_text = soup.get_text(separator=" ")

    processed = extract_meaningful(plain_text)

    # extract visual content (images)
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            if src.startswith("http"):
                images.append(src)
            else:
                images.append(url.rstrip("/") + "/" + src.lstrip("/"))

    return jsonify({
        "static": static_data,
        "dynamic": dynamic_data,
        "meaningful": processed,
        "images": images
    })

if __name__ == '__main__':
    app.run(debug=True)
