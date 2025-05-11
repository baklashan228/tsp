from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from Myshop.cruda import create_order as crud_create_order, read_orders as crud_read_orders, update_order as crud_update_order, delete_order as crud_delete_order  # Импортируйте ваш CRUD модуль

router = APIRouter()
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from Myshop.cruda import (
    create_order, read_orders,
    update_order, delete_order
)

logger = logging.getLogger(__name__)


@csrf_exempt
def orders_handler(request):
    """Обрабатывает GET и POST /orders/"""
    if request.method == 'GET':
        try:
            orders = read_orders()
            return JsonResponse({"orders": orders}, safe=False)
        except Exception as e:
            logger.error(f"GET orders error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Валидация
            required_fields = ['user_id', 'status', 'total_amount']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            order_id = create_order(
                user_id=data['user_id'],
                status=data['status'],
                total_amount=float(data['total_amount'])
            )

            return JsonResponse(
                {"message": "Order created", "order_id": order_id},
                status=201
            )
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"POST order error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def order_detail_handler(request, order_id):

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            valid_fields = ['status', 'total_amount']
            update_data = {k: v for k, v in data.items() if k in valid_fields}

            if not update_data:
                raise ValueError("No valid fields to update provided")

            if 'total_amount' in update_data:
                update_data['total_amount'] = float(update_data['total_amount'])

            updated = update_order(order_id, **update_data)

            if not updated:
                return JsonResponse({"error": "Order not found"}, status=404)

            return JsonResponse({"message": "Order updated"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"PUT order error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            deleted = delete_order(order_id)
            if not deleted:
                return JsonResponse({"error": "Order not found"}, status=404)
            return JsonResponse({"message": "Order deleted"})
        except Exception as e:
            logger.error(f"DELETE order error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)