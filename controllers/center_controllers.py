from database import db
from flask import request, render_template, g


def render_centers():
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, image, location, location_link, rating from centers")
    centers = cursor.fetchall()
    center_list = []

    for center in centers:
        center_list.append({
            "name": center[0],
            "image": center[1],
            "location": center[2],
            "location_link": center[3],
            "rating": center[4],
        })

    print(center_list)

    cursor.close()
    return render_template("centers.html", user=g.get("user_data"), centers=center_list, active_link="centers")
