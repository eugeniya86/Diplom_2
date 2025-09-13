import allure
from pages.order_page import Order_page


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_unauthorized_success(self):
        order = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        response = Order_page.create_order("", order)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert "order" in response.json()

    @allure.title("Создание заказа с авторизацией с ингредиентами")
    def test_create_order_authorized(self, registered_user):
        token = registered_user['response']['accessToken']
        order = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
        response = Order_page.create_order(token, order)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert "order" in response.json()

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        order = {"ingredients": []}
        response = Order_page.create_order("", order)
        assert response.status_code == 400

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self):
        order = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
        response = Order_page.create_order("", order)
        assert response.status_code == 500
