from Myshop.database import init_db
from typing import Optional
import uuid, psycopg2
from typing import Optional, Tuple
from sqlalchemy import DateTime
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
# Create User
def create_user(username: str, email: str, password_hash: str) -> bool:
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            '''INSERT INTO "User" (email, username, password_hash)
               VALUES (%s, %s, %s)
               RETURNING user_id''',
            (email, username, password_hash))

        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id

    except psycopg2.IntegrityError as e:
        if 'unique constraint "user_email_key"' in str(e):
            raise ValueError("Email already exists") from e
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()
# Read Users
def read_users():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "User"')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

# Update User
def update_user(user_id, **kwargs):
    """Обновляет данные пользователя"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Формируем динамический UPDATE запрос
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        if not set_clause:
            return False

        query = f'UPDATE "User" SET {set_clause} WHERE user_id = %s'
        params = list(kwargs.values()) + [user_id]

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def delete_user(user_id):
    """Удаляет пользователя"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM "User" WHERE user_id = %s',
            (user_id,)
        )
        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Create Category
async def create_category(category_id, name, description):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Category (category_id, name, description) VALUES (?, ?, ?)", (category_id, name, description))
    conn.commit()
    conn.close()
# Read Categories
def read_categories():
    conn = None
    try:
        conn = init_db()  # Пробуем подключиться к БД
        print("Database connection object:", conn)  # <-- Логируем соединение
        if conn is None:
            raise ValueError("Database connection failed")

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Category"')

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    except Exception as e:
        print(f"Database error in read_categories: {e}")
        raise
    finally:
        if conn:
            conn.close()
read_categories()
# Update Category
def update_category(category_id, name, description):
    conn = init_db()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            # Используем правильное имя столбца: category_id вместо id
            cursor.execute(
                'UPDATE "Category" SET name = %s, description = %s WHERE category_id = %s',
                (name, description, category_id)
            )
            conn.commit()  # Фиксируем изменения
            return cursor.rowcount > 0  # True, если запись обновлена
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
        return False
    finally:
        conn.close()

# Delete Category
def delete_category(category_id):
    conn = None
    try:
        conn = init_db()
        if not conn:
            return False

        with conn.cursor() as cursor:
            # Убедитесь, что имя столбца совпадает с БД (category_id или id)
            cursor.execute(
                'DELETE FROM "Category" WHERE category_id = %s',
                (category_id,)
            )
            deleted_rows = cursor.rowcount
            conn.commit()  # Важно: фиксируем изменения

            print(f"Deleted {deleted_rows} rows")
            return deleted_rows > 0

    except Exception as e:
        print(f"Delete error: {str(e)}", exc_info=True)
        return False
    finally:
        if conn:
            conn.close()
# Create Product
def create_product(name, description, price, stock, category_id):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # 1. Проверяем существование категории
        cursor.execute('SELECT 1 FROM "Category" WHERE category_id = %s', (category_id,))
        if not cursor.fetchone():
            raise ValueError("Данный продукт нельзя добавить, потому что такой категории не существует")

        # 2. Если категория существует, добавляем продукт
        cursor.execute(
            'INSERT INTO "Product" (name, description, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)',
            (name, description, price, stock, category_id)
        )
        conn.commit()
        return True

    except Exception as e:
        if conn:
            conn.rollback()  # Откатываем изменения при ошибке
        raise e  # Пробрасываем исключение дальше
    finally:
        if conn:
            conn.close()  # Всегда закрываем соединение
# Read Products
def read_products():
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Для PostgreSQL используем двойные кавычки для имён таблиц
        cursor.execute('SELECT * FROM "Product"')

        # Преобразуем результат в список словарей
        columns = [col[0] for col in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return products if products else []  # Возвращаем пустой список, если нет данных

    except Exception as e:
        print(f"Database error in read_products: {str(e)}")
        raise  # Пробрасываем исключение для обработки в view
    finally:
        if conn:
            conn.close()
# Update Product
def update_product(product_id, **fields):
    """Обновляет данные продукта"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Проверяем, что есть что обновлять
        if not fields:
            return False

        # Формируем динамический запрос
        set_clause = ", ".join([f'"{k}" = %s' for k in fields.keys()])
        query = f"""
            UPDATE "Product" 
            SET {set_clause}
            WHERE product_id = %s
        """

        # Параметры в правильном порядке: значения полей + product_id
        params = list(fields.values()) + [product_id]

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Update product error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
# Delete Product
def delete_product(product_id):
    """Удаляет продукт из базы данных с проверкой существования"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Сначала проверяем существование продукта
        cursor.execute('SELECT 1 FROM "Product" WHERE product_id = %s', (product_id,))
        if not cursor.fetchone():
            return False  # Продукт не найден

        # Удаляем продукт
        cursor.execute('DELETE FROM "Product" WHERE product_id = %s', (product_id,))
        conn.commit()
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Delete product error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
# Create Review
def create_review(product_id, user_id, rating, comment):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Review (product_id, user_id, rating, comment) VALUES (?, ?, ?, ?)",
                   (product_id, user_id, rating, comment))
    conn.commit()
    conn.close()

# Read Reviews
def read_reviews():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Review")
    reviews = cursor.fetchall()
    conn.close()
    return reviews

# Update Review
def update_review(review_id, rating, comment):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Review SET rating = ?, comment = ? WHERE review_id = ?", (rating, comment, review_id))
    conn.commit()
    conn.close()

    # Delete Review


def delete_review(review_id):
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Review WHERE review_id = ?", (review_id,))
    conn.commit()
    conn.close()

# Create Order
# Создание заказа
from contextlib import contextmanager


def create_order(user_id: int, status: str = "pending") -> int:
    """
    Создает новый заказ в базе данных.

    Args:
        user_id: Идентификатор пользователя
        status: Статус заказа (по умолчанию "pending")

    Returns:
        Идентификатор созданного заказа (order_id)
    """

    @contextmanager
    def get_cursor():
        """Контекстный менеджер для управления подключением"""
        conn = None
        try:
            conn = init_db()
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    try:
        with get_cursor() as cursor:
            # Исправленный запрос (total_amount удален из INSERT)
            cursor.execute(
                """
                INSERT INTO "Order" (user_id, status)
                VALUES (%s, %s)
                RETURNING order_id
                """,
                (user_id, status)
            )
            order_id = cursor.fetchone()[0]
            return order_id

    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise RuntimeError("Failed to create order") from e


# Получение списка заказов
def read_orders():
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.order_id, o.user_id, o.order_date, o.status, o.total_amount,
                   u.username as user_name
            FROM "Order" o
            JOIN "User" u ON o.user_id = u.user_id
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()



# Обновление заказа
def update_order(order_id, **fields):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        if not fields:
            return False

        set_clause = ", ".join([f'"{k}" = %s' for k in fields.keys()])
        query = f"""
            UPDATE "Order" 
            SET {set_clause}
            WHERE order_id = %s
        """
        params = list(fields.values()) + [order_id]

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Удаление заказа
def delete_order(order_id):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Сначала удаляем связанные OrderItem
        cursor.execute('DELETE FROM "Orderitem" WHERE order_id = %s', (order_id,))

        # Затем удаляем сам заказ
        cursor.execute('DELETE FROM "Order" WHERE order_id = %s', (order_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Создание OrderItem

# Получение всех элементов заказа
def get_order_items(order_id=None):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        query = """
            SELECT oi.*, p.name as product_name, p.description as product_description
            FROM "Orderitem" oi
            JOIN "Product" p ON oi.product_id = p.product_id
        """
        params = ()

        if order_id:
            query += " WHERE oi.order_id = %s"
            params = (order_id,)

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


# Обновление OrderItem
def update_order_item(order_item_id, **fields):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        if not fields:
            return False

        set_clause = ", ".join([f'"{k}" = %s' for k in fields.keys()])
        query = f"""
            UPDATE "Orderitem" 
            SET {set_clause}
            WHERE order_item_id = %s
        """
        params = list(fields.values()) + [order_item_id]

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Удаление OrderItem
def delete_order_item(order_item_id):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM "Orderitem" WHERE order_item_id = %s',
            (order_item_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Создание отзыва
def create_review(product_id, user_id, rating, comment=None):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Проверка существования продукта и пользователя
        cursor.execute('SELECT 1 FROM "Product" WHERE product_id = %s', (product_id,))
        if not cursor.fetchone():
            raise ValueError("Product not found")

        cursor.execute('SELECT 1 FROM "User" WHERE user_id = %s', (user_id,))
        if not cursor.fetchone():
            raise ValueError("User not found")

        cursor.execute(
            """INSERT INTO "Review" 
            (product_id, user_id, rating, comment) 
            VALUES (%s, %s, %s, %s) RETURNING review_id""",
            (product_id, user_id, rating, comment)
        )
        review_id = cursor.fetchone()[0]
        conn.commit()
        return review_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# Получение отзывов
def get_reviews(product_id=None, user_id=None):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        query = """
            SELECT r.*, 
                   p.name as product_name,
                   u.username as user_name
            FROM "Review" r
            JOIN "Product" p ON r.product_id = p.product_id
            JOIN "User" u ON r.user_id = u.user_id
        """
        conditions = []
        params = []

        if product_id:
            conditions.append("r.product_id = %s")
            params.append(product_id)
        if user_id:
            conditions.append("r.user_id = %s")
            params.append(user_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


# Обновление отзыва
def update_review(review_id, **fields):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        if not fields:
            return False

        set_clause = ", ".join([f'"{k}" = %s' for k in fields.keys()])
        query = f"""
            UPDATE "Review" 
            SET {set_clause}
            WHERE review_id = %s
        """
        params = list(fields.values()) + [review_id]

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


import logging

logger = logging.getLogger(__name__)


def get_user_orders_structure(user_id):
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return {"user_id": user_id, "orders": [], "error": "DB connection failed"}

        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                "Order".order_id,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'order_item_id', "Orderitem".order_item_id,
                            'product_id', "Orderitem".product_id,
                            'product_name', "Product".name,
                            'category_id', "Product".category_id,
                            'quantity', "Orderitem".quantity
                        )
                    ) FILTER (WHERE "Orderitem".order_item_id IS NOT NULL),
                    '[]'::json
                ) AS items,
                COALESCE(SUM("Order".total_amount), 0) AS total_amount
            FROM "Order"
            LEFT JOIN "Orderitem" ON "Order".order_id = "Orderitem".order_id
            LEFT JOIN "Product" ON "Orderitem".product_id = "Product".product_id
            WHERE "Order".user_id = %s
            GROUP BY "Order".order_id
            ORDER BY "Order".order_id DESC
        """, (user_id,))

        orders = []
        for row in cursor.fetchall():
            orders.append({
                "order_id": row[0],
                "items": row[1],
                "total_amount": row[2]  # Добавляем total_amount в структуру заказа
            })

        return {
            "user_id": user_id,
            "orders": orders,
            "message": "No orders found" if not orders else None
        }

    except Exception as e:
        logger.error(f"Error in get_user_orders_structure: {str(e)}", exc_info=True)
        return {
            "user_id": user_id,
            "orders": [],
            "error": str(e)
        }

    finally:
        if conn:
            conn.close()



def get_or_create_pending_order(user_id: int) -> Optional[int]:
    """Находит или создает заказ со статусом 'pending'"""
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return None

        with conn.cursor() as cursor:
            # Поиск существующего заказа
            cursor.execute(
                """
                SELECT order_id 
                FROM "Order" 
                WHERE user_id = %s 
                AND status = 'pending' 
                ORDER BY order_date DESC 
                LIMIT 1
                """,
                (user_id,)
            )
            order = cursor.fetchone()

            if not order:
                # Создание нового заказа
                cursor.execute(
                    """
                    INSERT INTO "Order" (user_id, status, total_amount)
                    VALUES (%s, 'pending', 0)
                    RETURNING order_id
                    """,
                    (user_id,)
                )
                order = cursor.fetchone()
                conn.commit()

            return order[0] if order else None

    except Exception as e:
        logger.error(f"Error in get_or_create_pending_order: {str(e)}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def get_product_price(product_id: int) -> Optional[float]:
    """Возвращает цену товара из базы"""
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return None

        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT price FROM "Product" WHERE product_id = %s',
                (product_id,)
            )
            product = cursor.fetchone()
            return float(product[0]) if product else None

    except Exception as e:
        logger.error(f"Error in get_product_price: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()


# crud.py
def create_order_item(order_id: int, product_id: int, quantity: int, price: float) -> int:
    """Добавляет или обновляет позицию в заказе"""
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return None

        with conn.cursor() as cursor:
            # 1. Попытка обновить существующую позицию
            cursor.execute(
                """
                UPDATE "Orderitem" 
                SET quantity = quantity + %s
                WHERE order_id = %s AND product_id = %s
                RETURNING order_item_id
                """,
                (quantity, order_id, product_id)
            )
            updated_item = cursor.fetchone()

            # 2. Если позиция не найдена - создаем новую
            if not updated_item:
                cursor.execute(
                    """
                    INSERT INTO "Orderitem" (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                    RETURNING order_item_id
                    """,
                    (order_id, product_id, quantity, price)
                )
                updated_item = cursor.fetchone()

            # 3. Обновляем общую сумму заказа
            cursor.execute(
                """
                UPDATE "Order" 
                SET total_amount = total_amount + (%s * %s)
                WHERE order_id = %s
                """,
                (quantity, price, order_id)
            )

            conn.commit()
            return updated_item[0]

    except Exception as e:
        logger.error(f"Error in create_or_update_order_item: {str(e)}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()
# crud.py
def check_user_exists(user_id: int) -> bool:
    """Проверяет существование пользователя в базе"""
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return False

        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT 1 FROM "User" WHERE user_id = %s',
                (user_id,)
            )
            return bool(cursor.fetchone())

    except Exception as e:
        logger.error(f"Error in check_user_exists: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()


def get_max_user_id() -> int:
    """
    Возвращает максимальный user_id из таблицы User.
    Возвращает 0, если таблица пуста или произошла ошибка.
    """
    conn = None
    try:
        conn = init_db()
        if not conn:
            logger.error("Database connection failed")
            return 0

        with conn.cursor() as cursor:
            # Выполняем SQL-запрос
            cursor.execute("SELECT MAX(user_id) FROM \"User\"")
            result = cursor.fetchone()

            # Обрабатываем результат
            max_id = result[0] if result else 0
            return max_id if max_id is not None else 0

    except Exception as e:
        logger.error(f"Error getting max user_id: {str(e)}")
        return 0
    finally:
        if conn:
            conn.close()


def create_user_session(user_id: int) -> Optional[str]:
    """Создание новой сессии пользователя"""
    conn = None
    try:
        session_id = str(uuid.uuid4())
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            '''INSERT INTO public.session (session_id, user_id)
               VALUES (%s, %s)''',
            (session_id, user_id))
        conn.commit()
        return session_id

    except psycopg2.IntegrityError:
        print("Session ID collision, retrying...")
        return create_user_session(user_id)  # Рекурсия при коллизии
    except psycopg2.Error as e:
        print(f"Session creation error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_user_by_email(email: str) -> Optional[Tuple]:
    """Получение пользователя по email"""
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT user_id, username, password_hash FROM "User" WHERE email = %s',
            (email,)
        )
        return cursor.fetchone()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def verify_password(hash_password: str, stored_password: str) -> bool:
    return hash_password == stored_password