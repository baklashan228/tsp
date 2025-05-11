from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from Myshop.cruda import (
    create_review, get_reviews,
    update_review, delete_review
)

logger = logging.getLogger(__name__)


@csrf_exempt
def reviews_handler(request):
    """Обрабатывает GET и POST /reviews/"""
    if request.method == 'GET':
        try:
            reviews = get_reviews()
            return JsonResponse({"reviews": reviews}, safe=False)
        except Exception as e:
            logger.error(f"GET reviews error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Валидация
            required_fields = ['product_id', 'user_id', 'rating']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            if not 1 <= int(data['rating']) <= 5:
                raise ValueError("Rating must be between 1 and 5")

            review_id = create_review(
                product_id=data['product_id'],
                user_id=data['user_id'],
                rating=int(data['rating']),
                comment=data.get('comment')
            )

            return JsonResponse(
                {"message": "Review created", "review_id": review_id},
                status=201
            )
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"POST review error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def review_detail_handler(request, review_id):
    """Обрабатывает GET, PUT, DELETE /reviews/<id>/"""
    if request.method == 'GET':
        try:
            reviews = get_reviews()
            review = next((r for r in reviews if r['review_id'] == review_id), None)
            if not review:
                return JsonResponse({"error": "Review not found"}, status=404)
            return JsonResponse({"review": review})
        except Exception as e:
            logger.error(f"GET review error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            valid_fields = ['rating', 'comment']
            update_data = {k: v for k, v in data.items() if k in valid_fields}

            if not update_data:
                raise ValueError("No valid fields to update provided")

            if 'rating' in update_data:
                rating = int(update_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                update_data['rating'] = rating

            updated = update_review(review_id, **update_data)

            if not updated:
                return JsonResponse({"error": "Review not found"}, status=404)

            return JsonResponse({"message": "Review updated"})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"PUT review error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            deleted = delete_review(review_id)
            if not deleted:
                return JsonResponse({"error": "Review not found"}, status=404)
            return JsonResponse({"message": "Review deleted"})
        except Exception as e:
            logger.error(f"DELETE review error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def product_reviews_handler(request, product_id):
    """Обрабатывает GET /products/<product_id>/reviews/"""
    if request.method == 'GET':
        try:
            reviews = get_reviews(product_id=product_id)
            return JsonResponse({"reviews": reviews}, safe=False)
        except Exception as e:
            logger.error(f"GET product reviews error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def user_reviews_handler(request, user_id):
    """Обрабатывает GET /users/<user_id>/reviews/"""
    if request.method == 'GET':
        try:
            reviews = get_reviews(user_id=user_id)
            return JsonResponse({"reviews": reviews}, safe=False)
        except Exception as e:
            logger.error(f"GET user reviews error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)