import requests
import json

headers = {
    'authority': 'shopee.vn',
    'x-requested-with': 'XMLHttpRequest',
    'if-none-match-': '55b03-d52c6fa8cb48e98b62aa62ad1dde6c3b',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-api-source': 'pc',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'
}

def getProduct(category_id, limit):
    params = (
        ('by', 'pop'),
        ('limit', limit),
        ('match_id', category_id),
        ('newest', '0'),
        ('order', 'desc'),
        ('page_type', 'search'),
        ('version', '2'),
    )

    response = requests.get('https://shopee.vn/api/v2/search_items/', headers=headers, params=params)

    return json.loads(response.text)