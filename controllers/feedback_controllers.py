from flask import render_template, g, request, redirect
from utils.validator import Validator
from database import db


def create_feedback():
    data = request.form
    cursor = db.cursor()
    validator = (Validator(data)
                 .field("feedback")
                 .required("please enter your feedback")
                 .max_length(1000, "feedback must be less than 1000 words")
                #  .min_length(100, "feedback must be more than 100 words")
                 .field("user_id")
                 .required("please provide the user id"))
                 
    try:
        if validator.errors.__len__() > 0:
            return render_template("feedback.html", errors=validator.errors, **validator.data, user=g.get("user_data"))

        feedback = data.get("feedback")
        user_id  = data.get("user_id")
       

        cursor.execute(
            "INSERT INTO feedback(feedback, user_id) VALUES(%s, %s)",
            (feedback, user_id)
        )

        cursor.close()
        db.commit()

        return render_template("feedback-confirmation.html", user=g.get("user_data"))
    except Exception as err:
        print(err)
        return redirect("/")

