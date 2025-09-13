import allure
from pages.order_page import Order_page


class TestUserOrders:
    def test_get_orders_authorized_with_orders(self, registered_user_with_order):
        token = registered_user_with_order['token']
        response = Order_page.get_user_orders(token)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert len(response_data['orders']) > 0
        first_order = response_data['orders'][0]
        required_fields = ['number', 'ingredients', 'status', 'createdAt', 'updatedAt', 'name']
        for field in required_fields:
            assert field in first_order, f"Заказ должен содержать поле {field}"

    @allure.title("Получение заказов авторизованного пользователя без заказов")
    def test_get_orders_authorized_no_orders(self, registered_user):
        token = registered_user['response']['accessToken']
        response = Order_page.get_user_orders(token)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert len(response_data['orders']) == 0

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = Order_page.get_user_orders(None)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert response_data['message'] == "You should be authorised"
