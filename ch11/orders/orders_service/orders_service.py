from orders.orders_service.exceptions import OrderNotFoundError
from orders.repository.orders_repository import OrdersRepository


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    def place_order(self, items, user_id):
        return self.orders_repository.add(items, user_id)

    def get_order(self, order_id, **filters):  # ← **filtersでuser_idを受け取る
        order = self.orders_repository.get(
            order_id, **filters  # ← **filtersをそのまま渡す
        )
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with id {order_id} not found")

    def update_order(self, order_id, user_id, **payload):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return self.orders_repository.update(order_id, **payload)

    def list_orders(self, **filters):
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit=limit, **filters)

    def pay_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id, status="progress", schedule_id=schedule_id
        )

    def cancel_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        order.cancel()
        return self.orders_repository.update(order_id, status="cancelled")

    def delete_order(self, order_id, user_id):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        return self.orders_repository.delete(order_id)
