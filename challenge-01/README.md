# Name - Coupon hijack

You're shopping at FlashDeals, an online store with amazing discounts. The **Golden Trophy** costs $1,000, but you only have $50.

A friend who works there told you about a secret admin coupon `ADMIN99` that gives 99% off. When you try to use it, the system blocks you saying "Admin coupon not allowed."

**Goal:** Buy the trophy for under $50

## Start the challenge

### Option 1: Docker (recommended)

```bash
docker-compose up
```

### Option 2: pipenv

```bash
pipenv shell
pipenv install
python3 app.py
```

## Available Coupons

- `SAVE10` - 10% off
- `SAVE25` - 25% off
- `SAVE50` - 50% off
- `ADMIN99` - 99% off (admin only)

## Example Request

```bash
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{"item": "trophy", "coupon": "SAVE50"}'
```

This gives you 50% off ($500), but you need to get it under $50...

## References

- [Bishop Fox: JSON Interoperability Vulnerabilities](https://bishopfox.com/blog/json-interoperability-vulnerabilities)
- [RFC 8259: JSON Specification](https://tools.ietf.org/html/rfc8259) (Section 4 on duplicate keys)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
