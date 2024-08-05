from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime
from flaskr.formSchema import sections, profileInputs
from flaskr.visitors import get_visitor_count
from flaskr.common import (
    get_all_messages,
    get_db,
    get_messages,
    get_profiles,
    get_values,
    getProfileData,
)

bp = Blueprint("blog", __name__)


@bp.route("/")
@login_required
def index():
    count = get_visitor_count()
    profiles = get_profiles()
    return render_template("blog/index.html", args=profiles, visitor_count=count)


@bp.route("/<username>/profile/view", methods=("GET",))
@login_required
def viewProfile(username):
    count = get_visitor_count()
    profileData = getProfileData(username)
    return render_template(
        "blog/profile.html",
        username=username,
        profileData=profileData,
        sections=sections,
        profileInputs=profileInputs,
        visitor_count=count,
    )


@bp.route("/<username>/profile/edit", methods=("GET", "POST"))
@login_required
def editProfile(username):
    if g.user["username"] != username:
        abort(403, f"Unauthorized!")

    count = get_visitor_count()
    profileData = getProfileData(username)

    if request.method == "POST":
        db = get_db()
        db.execute(
            "UPDATE client SET clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ?"
            f"WHERE token = '{username}'",
            (
                request.form["clientGender"],
                request.form["clientCast"],
                request.form["clientOccupation"],
                request.form["clientEducation"],
                int(request.form["clientAge"]),
                float(request.form["clientHeight"]),
                request.form["clientComplexion"],
            ),
        )
        db.execute(
            "UPDATE preference SET preferenceGender = ?, preferenceOccupation = ?, preferenceEducation = ?, preferenceAge = ?, preferenceHeight = ?, preferencecomplexion = ?"
            f"WHERE token = '{username}'",
            (
                "Female" if request.form["clientGender"] == "Male" else "Male",
                request.form["preferenceOccupation"],
                request.form["preferenceEducation"],
                int(request.form["preferenceAge"]),
                float(request.form["preferenceHeight"]),
                request.form["preferenceComplexion"],
            ),
        )
        db.execute(
            "UPDATE parents SET fathersOccupation = ?, mothersOccupation = ?, mothersCast = ?, otherRelations = ?"
            f"WHERE token = '{username}'",
            (
                request.form["fathersOccupation"],
                request.form["mothersOccupation"],
                request.form["mothersCast"],
                request.form["otherRelations"],
            ),
        )
        db.execute(
            "UPDATE lifestyle SET smoking = ?, prayers = ?, religiousSect = ?"
            f"WHERE token = '{username}'",
            (
                request.form["smoking"],
                request.form["prayers"],
                request.form["religiousSect"],
            ),
        )
        db.execute(
            "UPDATE residence SET presentAddress = ?, oldAddress = ?"
            f"WHERE token = '{username}'",
            (
                request.form["presentAddress"],
                request.form["oldAddress"],
            ),
        )
        db.execute(
            "UPDATE sibling SET siblingGender = ?, siblingOccupation = ?, siblingSpouseCast = ?, siblingSpouseOccupation = ?"
            f"WHERE token = '{username}'",
            (
                request.form["siblingGender"],
                request.form["siblingOccupation"],
                request.form["siblingSpouseCast"],
                request.form["siblingSpouseOccupation"],
            ),
        )
        db.commit()
        flash("Details saved successfully")
        return redirect(url_for("blog.viewProfile", username=username))

    return render_template(
        "blog/profile.html",
        username=username,
        profileData=profileData,
        sections=sections,
        profileInputs=profileInputs,
        visitor_count=count,
    )


@bp.route("/<username>/profile/create", methods=("GET", "POST"))
@login_required
def createProfile(username):
    if g.user["username"] != username:
        abort(403, f"Unauthorized!")

    count = get_visitor_count()
    profile = get_values(username, "client")

    if profile:
        return redirect(url_for("blog.viewProfile", username=username))
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO client (clientGender, token, clientCast, clientOccupation, clientEducation, clientAge, clientHeight, clientComplexion)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                request.form["clientGender"],
                username,
                request.form["clientCast"],
                request.form["clientOccupation"],
                request.form["clientEducation"],
                int(request.form["clientAge"]),
                float(request.form["clientHeight"]),
                request.form["clientComplexion"],
            ),
        )
        db.execute(
            "INSERT INTO preference (preferenceGender, token, preferenceOccupation, preferenceEducation, preferenceAge, preferenceHeight, preferencecomplexion)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "Female" if request.form["clientGender"] == "Male" else "Male",
                username,
                request.form["preferenceOccupation"],
                request.form["preferenceEducation"],
                int(request.form["preferenceAge"]),
                float(request.form["preferenceHeight"]),
                request.form["preferenceComplexion"],
            ),
        )
        db.execute(
            "INSERT INTO parents (token, fathersOccupation, mothersOccupation, mothersCast, otherRelations)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                username,
                request.form["fathersOccupation"],
                request.form["mothersOccupation"],
                request.form["mothersCast"],
                request.form["otherRelations"],
            ),
        )
        db.execute(
            "INSERT INTO lifestyle (token, smoking, prayers, religiousSect)"
            " VALUES (?, ?, ?, ?)",
            (
                username,
                request.form["smoking"],
                request.form["prayers"],
                request.form["religiousSect"],
            ),
        )
        db.execute(
            "INSERT INTO residence (token, presentAddress, permanentAddress, oldAddress)"
            " VALUES (?, ?, ?, ?)",
            (
                username,
                request.form["presentAddress"],
                request.form["permanentAddress"],
                request.form["oldAddress"],
            ),
        )
        db.execute(
            "INSERT INTO sibling (token, siblingGender, siblingOccupation, siblingSpouseCast, siblingSpouseOccupation)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                username,
                request.form["siblingGender"],
                request.form["siblingOccupation"],
                request.form["siblingSpouseCast"],
                request.form["siblingSpouseOccupation"],
            ),
        )
        db.commit()
        flash("Details saved successfully")
        return redirect(url_for("blog.viewProfile", username=username))

    return render_template(
        "blog/profile.html",
        username=username,
        sections=sections,
        profileInputs=profileInputs,
        visitor_count=count,
    )


@bp.route("/<username>/profile/delete", methods=("POST",))
@login_required
def deleteProfile(username):
    if g.user["username"] != username:
        abort(403, f"Unauthorized!")
    profile = get_values(username, "client")
    if not profile is None:
        db = get_db()
        db.execute(
            f"DELETE FROM client WHERE token = '{username}'",
        )
        db.execute(
            f"DELETE FROM lifestyle WHERE token = '{username}'",
        )
        db.execute(
            f"DELETE FROM parents WHERE token = '{username}'",
        )
        db.execute(
            f"DELETE FROM preference WHERE token = '{username}'",
        )
        db.execute(
            f"DELETE FROM residence WHERE token = '{username}'",
        )
        db.execute(
            f"DELETE FROM sibling WHERE token = '{username}'",
        )
        db.commit()
        flash("Deleted successfully")
    return redirect(url_for("blog.index"))


@bp.route("/<username>/messages", methods=("GET", "POST"))
@login_required
def messages(username):
    interactions = get_all_messages(username)
    count = get_visitor_count()
    return render_template(
        "blog/index.html", username=username, args=interactions, visitor_count=count
    )


@bp.route("/<username>/message", methods=("GET", "POST"))
@login_required
def directMessage(username):
    count = get_visitor_count()
    recipientId = request.args.get("recipientId")
    size = request.args.get("size")
    recipient = (
        get_db()
        .execute(
            "SELECT u.*" f" FROM user u " f" WHERE u.id = '{recipientId}'",
        )
        .fetchone()
    )
    if request.method == "POST":
        message = request.form["messageBody"]
        db = get_db()
        db.execute(
            "INSERT INTO messages (senderId, recipientId, messageText, timeStamp)"
            " VALUES (?, ?, ?, ?)",
            (
                g.user["id"],
                recipientId,
                message,
                datetime.now(),
            ),
        )
        db.commit()

    messages = get_messages(g.user["id"], recipientId, size)

    return render_template(
        "blog/directMessage.html",
        username=username,
        messages=messages,
        receiver=recipient,
        size=size,
        visitor_count=count,
    )


@bp.route("/<username>/account", methods=("GET", "POST"))
@login_required
def account(username):
    # post = get_post(username)
    count = get_visitor_count()
    return render_template("blog/account.html", username=username, visitor_count=count)
