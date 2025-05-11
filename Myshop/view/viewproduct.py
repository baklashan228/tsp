from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from Myshop.cruda import (
    create_product,
    read_products,
    update_product,
    delete_product
)

logger = logging.getLogger(__name__)


@csrf_exempt
@csrf_exempt
def products_handler(request):
    if request.method == 'GET':
        try:
            logger.info("Attempting to fetch products...")
            products = read_products()
            logger.info(f"Fetched {len(products)} products")

            return JsonResponse(
                {"products": products},
                safe=False,
                status=200
            )

        except Exception as e:
            logger.error(f"GET products failed: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "Failed to load products", "details": str(e)},
                status=500
            )
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Проверка обязательных полей
            required_fields = ['name', 'price', 'stock', 'category_id']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            create_product(
                name=data['name'],
                description=data.get('description', ''),
                price=data['price'],
                stock=data['stock'],
                category_id=data['category_id']
            )

            return JsonResponse({"message": "Product created"}, status=201)

        except Exception as e:
            logger.error(f"POST product error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def product_detail_handler(request, product_id):
    """Обрабатывает PUT и DELETE /products/<id>/"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Проверка наличия полей для обновления
            if not any(key in data for key in ['price', 'stock']):
                raise ValueError("Must provide at least one field to update (price or stock)")

            # Преобразование типов
            update_fields = {}
            if 'price' in data:
                try:
                    update_fields['price'] = float(data['price'])
                except (TypeError, ValueError):
                    raise ValueError("Price must be a number")

            if 'stock' in data:
                try:
                    update_fields['stock'] = int(data['stock'])
                except (TypeError, ValueError):
                    raise ValueError("Stock must be an integer")

            # Вызов CRUD-функции
            updated = update_product(
                product_id=product_id,
                **update_fields
            )

            if not updated:
                return JsonResponse({"error": "Product not found"}, status=404)

            return JsonResponse({"message": "Product updated successfully"})

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"PUT product error: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)

    elif request.method == 'DELETE':
        try:
            deleted = delete_product(product_id)
            if not deleted:
                return JsonResponse({"error": "Product not found"}, status=404)
            return JsonResponse({"message": "Product deleted"})
        except Exception as e:
            logger.error(f"DELETE product error: {str(e)}", exc_info=True)
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)