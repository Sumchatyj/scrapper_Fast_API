import requests
from typing import Union


def fetch_data(nm_id: str) -> Union[dict, None]:
    response = requests.get(f"https://card.wb.ru/cards/detail?nm={nm_id}").\
        json().get('data').get('products')
    if not response:
        return None
    return response[0]
