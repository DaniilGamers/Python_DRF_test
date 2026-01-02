
currency_rates = {
    "USD": 38,
    "EUR": 41,
    "UAH": 1
   }


def convert_to_uah(price: int, currency: str):
    rate = currency_rates[currency]
    return price * rate, rate
