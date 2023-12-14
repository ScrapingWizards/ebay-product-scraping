def clean_price(price_with_currency):
    parts = price_with_currency.split()
    numeric_part = parts[1]
    numeric_part = numeric_part.replace(',', '.')
    price = float(numeric_part)
    return price
