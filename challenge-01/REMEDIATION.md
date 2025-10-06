# How to Fix It

## The Problem

The code parses the same JSON input in two different ways:

```python
# Custom string parsing (gets first value)
first_coupon = get_first_value(raw_data, 'coupon')

# Standard JSON parsing (gets last value)
coupon_from_dict = data.get('coupon')
```

This inconsistency creates a bypass opportunity.

## Solution: Use Schema Validation

```python
from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
import json

class CheckoutSchema(Schema):
    item = fields.Str(required=True)
    coupon = fields.Str(required=True)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Detect duplicate keys before parsing
    raw = request.get_data(as_text=True)
    if raw.count('"coupon"') > 1:
        return jsonify({"error": "Duplicate keys not allowed"}), 400

    # Validate with schema
    schema = CheckoutSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Now safe to process
    item = data['item'].lower()
    coupon = data['coupon'].upper()

    if item not in PRODUCTS:
        return jsonify({"error": "Item not found"}), 404

    if coupon == 'ADMIN99':
        return jsonify({"error": "Admin coupon not allowed"}), 403

    # Apply discount
    discount = COUPONS.get(coupon, 0)
    final_price = PRODUCTS[item] * (1 - discount)

    return jsonify({
        "item": item,
        "original_price": PRODUCTS[item],
        "discount": f"{int(discount * 100)}%",
        "final_price": final_price
    })
```

**Why this works:**
- Explicitly rejects duplicate keys
- Single source of truth for parsing
- Industry-standard validation library
- Clear error messages

### Minimum Fix: Make Parsing Consistent

If you must keep both parsers, at least make them agree:

```python
def get_last_value(raw_json, key):
    """Extract last occurrence to match Python's behavior"""
    try:
        parts = raw_json.split(f'"{key}"')
        if len(parts) < 2:
            return None
        # Get the LAST occurrence instead of first
        value_part = parts[-1].split(':')[1].split(',')[0].split('}')[0]
        return value_part.strip().strip('"').upper()
    except:
        return None

# Then use it consistently
first_coupon = get_last_value(raw_data, 'coupon')  # Now matches dict behavior
```

**Why this is minimal:**
- Doesn't fix root cause
- Still fragile string parsing
- But at least prevents the bypass


