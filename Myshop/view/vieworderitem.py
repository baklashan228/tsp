from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from sympy.physics.units.util import quantity_simplify

from Myshop.cruda import (
    create_order_item, get_order_items,
    update_order_item, delete_order_item,
    get_or_create_pending_order,
    get_product_price,
    create_order_item, check_user_exists
)

logger = logging.getLogger(__name__)


@csrf_exempt
def order_items_handler(request):
    """Обрабатывает GET и POST /order-items/"""
    if request.method == 'GET':
        try:
            items = get_order_items()
            return JsonResponse({"order_items": items}, safe=False)
        except Exception as e:
            logger.error(f"GET order items error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Валидация
            required_fields = ['user_id', 'product_id', 'quantity']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            # Проверка существования пользователя и товара
            if not check_user_exists(data['user_id']):
                raise ValueError("User not found")

            price = get_product_price(data['product_id'])
            if not price:
                raise ValueError("Product not found")

            # Получаем или создаем заказ
            order_id = get_or_create_pending_order(data['user_id'])

            # Добавляем/обновляем позицию
            item_id = create_order_item(
                order_id=order_id,
                product_id=data['product_id'],
                quantity=data['quantity'],
                price=price
            )

            return JsonResponse({
                "message": "Order item processed",
                "order_id": order_id,
                "order_item_id": item_id,
                "action": "updated" if item_id else "created"
            }, status=201)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return JsonResponse({"error": "Internal server error"}, status=500)

        return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def order_item_detail_handler(request, order_item_id):
    """Обрабатывает GET, PUT, DELETE /order-items/<id>/"""
    if request.method == 'GET':
        try:
            items = get_order_items()
            item = next((i for i in items if i['order_item_id'] == order_item_id), None)
            if not item:
                return JsonResponse({"error": "Order item not found"}, status=404)
            return JsonResponse({"order_item": item})
        except Exception as e:
            logger.error(f"GET order item error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            valid_fields = ['quantity', 'price']
            update_data = {k: v for k, v in data.items() if k in valid_fields}

            if not update_data:
                raise ValueError("No valid fields to update provided")

            if 'quantity' in update_data:
                update_data['quantity'] = int(update_data['quantity'])
            if 'price' in update_data:
                update_data['price'] = float(update_data['price'])

            updated = update_order_item(order_item_id, **update_data)

            if not updated:
                return JsonResponse({"error": "Order item not found"}, status=404)

            return JsonResponse({"message": "Order item updated"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"PUT order item error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            deleted = delete_order_item(order_item_id)
            if not deleted:
                return JsonResponse({"error": "Order item not found"}, status=404)
            return JsonResponse({"message": "Order item deleted"})
        except Exception as e:
            logger.error(f"DELETE order item error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def order_specific_items_handler(request, order_id):
    """Обрабатывает GET /orders/<order_id>/items/"""
    if request.method == 'GET':
        try:
            items = get_order_items(order_id)
            return JsonResponse({"order_items": items}, safe=False)
        except Exception as e:
            logger.error(f"GET order items error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)