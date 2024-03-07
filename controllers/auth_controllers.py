from flask import redirect, request, render_template, session, g
from database import db
import bcrypt
import uuid
import mysql
from utils.validator import Validator
from utils.authentication import authenticate
import traceback


def signup():
    data = request.form
    cursor = db.cursor()
    validator = (Validator(data)
                 .field("firstname")
                 .required("Please enter your name")
                 .max_length(24, "firstname must be less than 24 characters")
                 .field("lastname")
                 .required("Please enter your lastname")
                 .max_length(24, "lastname must be less than 24 characters")
                 .field("mobile_number")
                 .required("Please enter your mobile number")
                 .match_pattern(r'^[0-9]{10}$', "Please enter a valid mobile number")
                 .field("password")
                 .required("Please enter a password")
                 .min_length(8, "Password must be of at least 8 characters"))
    try:
        if validator.errors.__len__() > 0:
            return render_template("signup.html", errors=validator.errors, **validator.data)

        firstname = data.get("firstname")
        lastname = data.get("lastname")
        password = data.get("password")
        mobile_number = data.get("mobile_number")

        random_id = str(uuid.uuid4()).replace('-', '')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        cursor.execute(
            "INSERT INTO users(id, firstname, lastname, mobile_number, password) VALUES(%s, %s, %s, %s, %s)",
            (random_id, firstname, lastname, mobile_number, hashed_password)
        )

        cursor.close()
        db.commit()

        session["user_id"] = random_id
        return redirect("/")
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return render_template("signup.html", errors={"mobile_number": "mobile number already exits"}, **validator.data)
        return redirect("/")
    except Exception as err:
        return redirect("/")


def login():
    data = request.form
    cursor = db.cursor()
    validator = (Validator(data)
                 .field("mobile_number")
                 .required("Please enter your mobile number")
                 .match_pattern(r'^[0-9]{10}$', "Please enter a valid mobile number")
                 .field("password")
                 .required("Please enter a password"))
    try:
        if validator.errors.__len__() > 0:
            return render_template("login.html", errors=validator.errors, **validator.data)

        cursor.execute(
            "SELECT id, password FROM users WHERE mobile_number=%s", [validator.data["mobile_number"]])

        data = cursor.fetchone()
        cursor.close()

        if data is None:
            return render_template("login.html", errors={"mobile_number": "mobile number doesn't exits"}, **validator.data)
        else:
            password = validator.data["password"].encode('utf-8')
            hashed_password = data[1].encode('utf-8')

            if bcrypt.checkpw(password, hashed_password):
                session["user_id"] = data[0]
                return redirect("/")
            else:
                return render_template("login.html", errors={"password": "password is incorrect"}, **validator.data)

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return render_template("signup.html", errors={"mobile_number": "mobile number already exits"}, **validator.data)
        return redirect("/")
    except Exception as err:
        print(err)
        return redirect("/")


@authenticate
def update_account():
    if g.get("user_data") is None:
        return redirect("/login")

    user = g.get("user_data")

    data = request.form
    cursor = db.cursor()

    validator = (Validator(data)
                 .field("firstname")
                 .required("Please enter your name")
                 .max_length(24, "firstname must be less than 24 characters")
                 .field("lastname")
                 .required("Please enter your lastname")
                 .max_length(24, "lastname must be less than 24 characters")
                 .field("mobile_number")
                 .required("Please enter your mobile number")
                 .match_pattern(r'^[0-9]{10}$', "Please enter a valid mobile number"))

    try:
        if validator.errors.__len__() > 0:
            return render_template("account.html", errors=validator.errors, **validator.data, user=g.get("user_data"))

        firstname = data.get("firstname")
        lastname = data.get("lastname")
        mobile_number = data.get("mobile_number")

        cursor.execute(
            "UPDATE users SET firstname=%s, lastname=%s, mobile_number =%s WHERE id=%s",
            (firstname, lastname, mobile_number, user['id'])
        )

        cursor.execute(
            "SELECT firstname, lastname, mobile_number FROM users WHERE id=%s", [user['id']])
        user_data = cursor.fetchall()[0]

        user = {
            "id": user['id'],
            "firstname": user_data[0],
            "lastname": user_data[1],
            "mobile_number": user_data[2],
        }

        cursor.close()
        db.commit()

        return render_template("account.html", **validator.data, user=user)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return render_template("account.html", errors={"mobile_number": "mobile number already exits"}, **validator.data, user=user)
        else:
            print(err)
            traceback.print_exc()
        return redirect("/")

    except Exception as err:
        print(err)
        traceback.print_exc()
        return redirect("/")
