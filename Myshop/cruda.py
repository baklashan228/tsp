from Myshop.database import init_db



# Create User
def create_user(user_id, username, email):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Правильный синтаксис для PostgreSQL:
        cursor.execute(
            'INSERT INTO "User" (user_id, username, email) VALUES (%s, %s, %s)',
            (user_id, username, email)
        )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
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
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "Product" (name, description, price, stock, category_id) VALUES (%s, %s, %s, %s, %s)',
                   (name, description, price, stock, category_id))
    conn.commit()
    conn.close()

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
def create_order(user_id, status, total_amount):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO "Order" 
            (user_id, status, total_amount) 
            VALUES (%s, %s, %s) RETURNING order_id""",
            (user_id, status, total_amount)
        )
        order_id = cursor.fetchone()[0]
        conn.commit()
        return order_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


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
def create_order_item(order_id, product_id, quantity, price):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()

        # Проверка существования заказа и продукта
        cursor.execute('SELECT 1 FROM "Order" WHERE order_id = %s', (order_id,))
        if not cursor.fetchone():
            raise ValueError("Order not found")

        cursor.execute('SELECT 1 FROM "Product" WHERE product_id = %s', (product_id,))
        if not cursor.fetchone():
            raise ValueError("Product not found")

        cursor.execute(
            """INSERT INTO "Orderitem" 
            (order_id, product_id, quantity, price) 
            VALUES (%s, %s, %s, %s) RETURNING order_item_id""",
            (order_id, product_id, quantity, price)
        )
        item_id = cursor.fetchone()[0]
        conn.commit()
        return item_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


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


# Удаление отзыва
def delete_review(review_id):
    conn = None
    try:
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM "Review" WHERE review_id = %s',
            (review_id,)
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