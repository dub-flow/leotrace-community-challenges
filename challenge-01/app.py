from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# product catalog
PRODUCTS = {
    "mug": 15,
    "shirt": 45,
    "trophy": 1000
}

# discount codes
COUPONS = {
    "SAVE10": 0.10,
    "SAVE25": 0.25,
    "SAVE50": 0.50,
    "ADMIN99": 0.99  # admin coupon
}

def get_first_value(raw_json, key):
    try:
        parts = raw_json.split(f'"{key}"')
        if len(parts) < 2:
            return None
        value_part = parts[1].split(':')[1].split(',')[0].split('}')[0]
        return value_part.strip().strip('"').upper()
    except:
        return None

@app.route('/')
def home():
    return """
    <h1>FlashDeals Shop</h1>
    <p>Try our coupons: SAVE10, SAVE25, SAVE50</p>
    <pre>
curl -X POST http://localhost:5000/checkout \\
  -H "Content-Type: application/json" \\
  -d '{"item": "trophy", "coupon": "SAVE10"}'
    </pre>
    """

@app.route('/checkout', methods=['POST'])
def checkout():
    raw_data = request.get_data(as_text=True)
    data = request.json
    item = data.get('item', '').lower()
    coupon_from_dict = data.get('coupon', '').upper()
    if item not in PRODUCTS:
        return jsonify({"error": "Item not found"}), 404
    price = PRODUCTS[item]
    first_coupon = get_first_value(raw_data, 'coupon')
    if first_coupon == 'ADMIN99':
        return jsonify({"error": "Admin coupon not allowed"}), 403
    discount = COUPONS.get(coupon_from_dict, 0)
    final_price = price * (1 - discount)

    response = {
        "item": item,
        "original_price": price,
        "discount": f"{int(discount * 100)}%",
        "final_price": final_price
    }

    if item == "trophy" and final_price < 50:
        response["success"] = "Congratulations! bravo"

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
