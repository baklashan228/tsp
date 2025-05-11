from django.urls import path
from . import viewcategory
from . import viewuser
from . import viewproduct
from . import vieworder
from . import vieworderitem
from . import viewreview

urlpatterns = [
    # Один путь для GET и POST
    path('categories/', viewcategory.categories_handler),

    # Отдельный путь для PUT/DELETE с параметром
    path('categories/<int:category_id>/', viewcategory.category_detail_handler),
    # Новые маршруты для пользователей
    path('users/', viewuser.users_handler),  # GET (список) и POST (создание)
    path('users/<int:user_id>', viewuser.user_detail_handler),
    # Новые маршруты для продуктов
    path('products/', viewproduct.products_handler),  # GET-список и POST-создание
    path('products/<int:product_id>/', viewproduct.product_detail_handler),  # PUT/DELETE
    path('order/', vieworder.orders_handler),
    path('orders/<int:order_id>/', vieworder.order_detail_handler),
    path('order-items/', vieworderitem.order_items_handler),  # GET-список и POST-создание
    path('order-items/<int:order_item_id>/', vieworderitem.order_item_detail_handler),  # GET/PUT/DELETE
    path('reviews/', viewreview.reviews_handler),  # GET-список и POST-создание
    path('reviews/<int:review_id>/', viewreview.review_detail_handler),  # GET/PUT/DELETE


]