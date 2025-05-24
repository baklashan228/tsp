from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import uuid
from werkzeug.security import check_password_hash
from .auth import hash_password  # Импорт функции хеширования

from Myshop.cruda import (
    create_user ,
    read_users as crud_read_users,
    update_user as crud_update_user,
    delete_user as crud_delete_user,
    get_max_user_id, get_user_by_email,  create_user_session, verify_password
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

            # Валидация
            required_fields = ['username', 'email', 'password_hash']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")



            # Создание пользователя (3 аргумента)
            success = create_user(
                username=data['username'],
                email=data['email'],
                password_hash=data['password_hash']
            )

            return JsonResponse({"message": "User created"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

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


@csrf_exempt
def login_user(request):
    """Обработчик аутентификации пользователя"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password_hash', '').strip()

            # Валидация входных данных
            if not all([email, password]):
                return JsonResponse(
                    {"error": "Email and password required"},
                    status=400
                )

            # Получение пользователя
            user = get_user_by_email(email)
            if not user:
                logger.warning(f"Login attempt for unknown user: {email}")
                return JsonResponse(
                    {"error": "Invalid credentialsssss"},
                    status=401
                )

            # Проверка пароля
            user_id, username, db_password_hash = user
            if not verify_password(password, db_password_hash):
                logger.warning(f"Invalid password for: {email}")
                return JsonResponse(
                    {"error": "Invalid credentials"},
                    status=401
                )

            # Создание сессии
            session_id = create_user_session(user_id)
            if not session_id:
                logger.error("Failed to create session")
                return JsonResponse(
                    {"error": "Internal server error"},
                    status=500
                )

            return JsonResponse({
                "message": "Login successful",
                "user_id": user_id,
                "session_id": session_id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "Internal server error"},
                status=500
            )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )

@csrf_exempt
def register_user(request):
    """Обработчик регистрации пользователя"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password_hash', '').strip()
            username = data.get('username', '').strip()

            # Валидация обязательных полей
            if not email or not password:
                return JsonResponse(
                    {"error": "Email and password required"},
                    status=400
                )

            # Хеширование пароля
            hashed_password = hash_password(password)

            try:
                # Создание пользователя через CRUD
                user_id = create_user(email, username, hashed_password)
                return JsonResponse(
                    {"message": "User created", "user_id": user_id},
                    status=201
                )

            except ValueError as e:
                return JsonResponse(
                    {"error": str(e)},
                    status=400
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON format"},
                status=400
            )

        except Exception as e:
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "Internal server error"},
                status=500
            )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )