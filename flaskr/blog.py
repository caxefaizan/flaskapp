from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import sqlite3
from datetime import datetime
import itertools
from flaskr.formSchema import sections, profileInputs

bp = Blueprint("blog", __name__)


@bp.route("/")
@login_required
def index():
    profiles = get_profiles()
    return render_template("blog/index.html", args=profiles)


@bp.route("/<username>/profile/view", methods=("GET",))
@login_required
def viewProfile(username):
    profile = get_values(username, "client")
    sibling = get_values(username, "sibling")
    parents = get_values(username, "parents")
    preference = get_values(username, "preference")
    lifestyle = get_values(username, "lifestyle")
    residence = get_values(username, "residence")

    return render_template(
        "blog/profile.html",
        username=username,
        profile=profile,
        sibling=sibling,
        parents=parents,
        preference=preference,
        lifestyle=lifestyle,
        residence=residence,
        sections=sections,
        profileInputs=profileInputs,
    )


@bp.route("/<username>/profile/edit", methods=("GET", "POST"))
@login_required
def editProfile(username):
    if g.user["username"] != username:
        abort(403, f"Unauthorized!")
    profile = get_values(username, "client")
    sibling = get_values(username, "sibling")
    parents = get_values(username, "parents")
    preference = get_values(username, "preference")
    lifestyle = get_values(username, "lifestyle")
    residence = get_values(username, "residence")

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
            "UPDATE residence SET presentAddress = ?, size = ?, oldAddress = ?"
            f"WHERE token = '{username}'",
            (
                request.form["presentAddress"],
                request.form["size"],
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
        profile=profile,
        sibling=sibling,
        parents=parents,
        preference=preference,
        lifestyle=lifestyle,
        residence=residence,
        sections=sections,
        profileInputs=profileInputs,
    )


@bp.route("/<username>/profile/create", methods=("GET", "POST"))
@login_required
def createProfile(username):
    if g.user["username"] != username:
        abort(403, f"Unauthorized!")
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
            "INSERT INTO residence (token, presentAddress, size, oldAddress)"
            " VALUES (?, ?, ?, ?)",
            (
                username,
                request.form["presentAddress"],
                request.form["size"],
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

    return render_template("blog/index.html", username=username, args=interactions)


@bp.route("/<username>/message", methods=("GET", "POST"))
@login_required
def directMessage(username):
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
    )


@bp.route("/<username>/account", methods=("GET", "POST"))
@login_required
def account(username):
    # post = get_post(username)

    return render_template("blog/account.html", username=username)


def get_messages(userId, receiver, size, check_author=True) -> sqlite3.Row:
    messageSize = int(size) * 5
    messages = (
        get_db()
        .execute(
            f"SELECT m.* FROM messages m WHERE (m.senderId = '{userId}' OR m.senderId = '{receiver}') AND (m.recipientId = '{receiver}' OR m.recipientId = '{userId}')"
            f" ORDER BY m.timeStamp DESC LIMIT {messageSize}"
        )
        .fetchmany(messageSize)
    )
    return messages


def get_all_messages(username, check_author=True) -> sqlite3.Row:
    db = get_db()
    receivedMessagesFrom = db.execute(
        f"SELECT DISTINCT senderId FROM messages WHERE recipientId = '{g.user['id']}'"
        " ORDER BY timeStamp DESC"
    ).fetchall()
    sentMessagesTo = db.execute(
        f"SELECT DISTINCT recipientId FROM messages WHERE senderId = '{g.user['id']}'"
    ).fetchall()
    senders = list(itertools.chain.from_iterable(receivedMessagesFrom))
    receivers = list(itertools.chain.from_iterable(sentMessagesTo))
    interactions = list(set(senders) | set(receivers))
    interactions = ",".join(map(str, interactions))
    interactions = db.execute(
        f"SELECT u.id, u.username, u.lastActivity FROM user u WHERE id in ({interactions})"
    ).fetchall()
    interactions = [row for row in interactions]
    return interactions


def get_values(username, table_name, check_author=True) -> sqlite3.Row:
    profile = (
        get_db()
        .execute(
            "SELECT c.*" f" FROM {table_name} c " f" WHERE c.token = '{username}'",
        )
        .fetchone()
    )

    # if profile:
    #     profile = (
    #         get_db()
    #         .execute(
    #             f"""
    #             SELECT c.*,
    #             s.sex AS sibling_sex,
    #             s.occupation AS sibling_occupation,
    #             s.spouseCast AS sibling_spouse_cast,
    #             p.fathersOccupation AS fathers_occupation,
    #             p.mothersOccupation AS mothers_occupation,
    #             p.mothersCast AS mothers_cast,
    #             l.smoking AS smoking_habit,
    #             l.prayers AS prayer_habit,
    #             l.religiousSect AS religious_sect,
    #             r.presentAddress AS present_address,
    #             r.oldAddress AS old_address,
    #             cp.clientCast,
    #             cp.occupation,
    #             cp.education,
    #             cp.age,
    #             cp.height,
    #             cp.complexion
    #             FROM client c
    #             LEFT JOIN sibling s ON c.preferenceToken = s.relatedToken
    #             LEFT JOIN parents p ON c.preferenceToken = p.relatedToken
    #             LEFT JOIN lifestyle l ON c.preferenceToken = l.relatedToken
    #             LEFT JOIN residence r ON c.preferenceToken = r.relatedToken
    #             LEFT JOIN client cp ON c.preferenceToken = cp.token
    #             WHERE c.token = {username}
    #         """
    #         )
    #         .fetchone()
    #     )

    return profile


def get_profiles(check_author=True) -> sqlite3.Row:
    db = get_db()
    profiles = db.execute(
        "SELECT c.*, r.presentAddress AS present_address, u.lastActivity as lastActivity, u.id, u.username"
        " FROM client c JOIN residence r ON c.token = r.token JOIN user u ON u.username = c.token"
        " ORDER BY lastActivity DESC"
    ).fetchall()
    return profiles
