import requests
from data import Url


class Order_page:
    @staticmethod
    def create_order(auth_token, ingredients_data):
        headers = {
            'Authorization': f'Bearer {auth_token}' if auth_token else None,
            'Content-Type': 'application/json'
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        response = requests.post(
            Url.BASE_URL + Url.ORDERS,
            headers=headers,
            json=ingredients_data
        )
        return response

    @staticmethod
    def get_user_orders(auth_token):

        headers = {
            'Authorization': f'Bearer {auth_token}' if auth_token else None,
            'Content-Type': 'application/json'
        }
        headers = {k: v for k, v in headers.items() if v is not None}

        response = requests.get(
            Url.BASE_URL + Url.ORDERS,
            headers=headers
        )
        return response
