from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from Myshop.cruda import (
    create_user as crud_create_user,
    read_users as crud_read_users,
    update_user as crud_update_user,
    delete_user as crud_delete_user
)
logger = logging.getLogger(__name__)

@csrf_exempt
def users_handler(request):
    """Обрабатывает GET и POST /users/"""
    if request.method == 'GET':
        try:
            users = crud_read_users()

            # Дополнительная проверка данных
            if not isinstance(users, list):
                raise ValueError("Users data is not a list")

            return JsonResponse(
                {"users": users},
                safe=False,
                status=200
            )

        except Exception as e:
            logger.error(f"GET users error: {str(e)}")
            return JsonResponse(
                {
                    "error": "Failed to load users",
                    "details": str(e)
                },
                status=500
            )

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            crud_create_user(
                data["user_id"],  # или "id" в зависимости от вашей модели
                data["username"],
                data["email"],
            )
            return JsonResponse({"message": "User created"}, status=201)
        except Exception as e:
            logger.error(f"POST user error: {str(e)}")
            return JsonResponse(
                {"error": str(e)},
                status=400
            )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def user_detail_handler(request, user_id):
    """Обрабатывает PUT и DELETE /users/<id>/"""
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Обновляем только переданные поля
            updated = crud_update_user(
                user_id,
                username=data.get("username"),  # .get() для опциональных полей
                email=data.get("email"),
            )

            if not updated:
                return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({"message": "User updated"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            deleted = crud_delete_user(user_id)
            if not deleted:
                return JsonResponse({"error": "User not found"}, status=404)
            return JsonResponse({"message": "User deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)