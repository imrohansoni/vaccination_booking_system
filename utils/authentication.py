from flask import session, g
from database import db
from functools import wraps


def authenticate(handler):
    @wraps(handler)
    def decorator_fun(*args, **kwargs):
        if 'user_id' in session:
            user_id = session["user_id"]
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, firstname, lastname, mobile_number, user_type FROM users WHERE id=%s", [user_id])
            user = cursor.fetchall()[0]
            g.user_data = {
                "id": user[0],
                "firstname": user[1],
                "lastname": user[2],
                "mobile_number": user[3],
                "user_type": user[4],
            }
            cursor.close()
        return handler(*args, **kwargs)
    return decorator_fun


# def authentication():
#     if 'user_id' in session:
#         user_id = session["user_id"]
#         cursor = db.cursor()
#         cursor.execute(
#             "SELECT firstname, lastname FROM users WHERE id=%s", [user_id])
#         name = cursor.fetchall()

#         (firstname, lastname) = name[0]
#         cursor.close()
#         return f"{firstname} {lastname}"
#     else:
#         return None
