import pytest
from pages.user_page import User_page
from pages.order_page import Order_page
from generators import UserGenerator


@pytest.fixture
def existing_user():
    return register_new_user()


@pytest.fixture
def registered_user():
    return register_new_user()

def register_new_user():
    user_data = UserGenerator.random_user()
    response = User_page.register(user_data)
    response_data = response.json()
    return {
        'data': user_data,
        'response': response_data
    }



@pytest.fixture
def auth_token(registered_user):
    return registered_user['response']['accessToken']


@pytest.fixture
def registered_user_with_order():
    user_data = UserGenerator.random_user()
    register_response = User_page.register(user_data)
    token = register_response.json()['accessToken']
    order_data = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
    order_response = Order_page.create_order(token, order_data)
    return {
        'user_data': user_data,
        'token': token,
        'order_response': order_response.json()
    }


@pytest.fixture
def created_order(auth_token):
    order_data = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
    response = Order_page.create_order(auth_token, order_data)
    return response.json()