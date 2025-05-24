from flask import Flask, request, jsonify
from flask_cors import CORS
from sites.daraz import get_daraz_results
from sites.ebay import get_ebay_results
from sites.amazon import get_amazon_results

app = Flask(__name__)
CORS(app)

def get_cheapest_two(all_results):
    return sorted(all_results, key=lambda x: x["price"])[:2]

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify([])

    daraz = get_daraz_results(query)
    ebay = get_ebay_results(query)
    amazon = get_amazon_results(query)
    
    all_results = daraz + ebay
    return jsonify(get_cheapest_two(all_results))

if __name__ == "__main__":
    app.run(debug=True)
