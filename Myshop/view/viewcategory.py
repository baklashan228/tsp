from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from Myshop.cruda import (
    create_category as crud_create_category,
    read_categories as crud_read_categories,
    update_category as crud_update_category,
    delete_category as crud_delete_category
)
logger = logging.getLogger(__name__)


@csrf_exempt
def categories_handler(request):
    """Обрабатывает GET и POST /categories/"""
    if request.method == 'GET':
        try:
            categories = crud_read_categories()

            # Дополнительная проверка данных
            if not isinstance(categories, list):
                raise ValueError("Categories data is not a list")

            return JsonResponse(
                {"categories": categories},
                safe=False,
                status=200
            )

        except Exception as e:
            logger.error(f"GET error: {str(e)}")
            return JsonResponse(
                {
                    "error": "Failed to load categories",
                    "details": str(e)
                },
                status=500
            )

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            crud_create_category(
                data["category_id"],
                data["name"],
                data["description"]
            )
            return JsonResponse({"message": "Created"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def category_detail_handler(request, category_id):
    """Обрабатывает PUT и DELETE /categories/<id>/"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated = crud_update_category(
                category_id,
                data["name"],
                data["description"]
            )
            if not updated:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"message": "Updated"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'DELETE':
        deleted = crud_delete_category(category_id)
        if not deleted:
            return JsonResponse({"error": "Not found"}, status=404)
        return JsonResponse({"message": "Deleted"})

    return JsonResponse({"error": "Method not allowed"}, status=405)