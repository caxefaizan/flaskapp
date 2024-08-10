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
    createUpdateProfileData,
    preRouteChecks,
    deleteProfileData,
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
    action = request.path.split("/")[-1]
    count, profileData = preRouteChecks(g, action, username)


    return render_template(
        "blog/profile.html",
        username=username,
        profileData=None if action == "create" else profileData,
        sections=sections,
        profileInputs=profileInputs,
        visitor_count=count,
    )


@bp.route("/<username>/profile/edit", methods=("GET", "POST"))
@login_required
def editProfile(username):
    action = request.path.split("/")[-1]
    count, profileData = preRouteChecks(g, action, username)

    if request.method == "POST":
        createUpdateProfileData(username, request.form, action)
        flash("Details saved successfully")
        return redirect(url_for("blog.viewProfile", username=username, action=action))

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
    action = request.path.split("/")[-1]
    count, profileData = preRouteChecks(g, action, username)

    if request.method == "POST":
        createUpdateProfileData(username, request.form, action)
        flash("Details saved successfully")
        return redirect(url_for("blog.viewProfile", username=username, action=action))

    if profileData[0]:
        return redirect(url_for("blog.viewProfile", username=username, action=action))

    return render_template(
        "blog/profile.html",
        username=username,
        profileData=None,
        sections=sections,
        profileInputs=profileInputs,
        visitor_count=count,
    )


@bp.route("/<username>/profile/delete", methods=("POST",))
@login_required
def deleteProfile(username):
    action = request.path.split("/")[-1]
    _, profileData = preRouteChecks(g, action, username)

    if not profileData[0] is None:
        db = get_db()
        deleteProfileData(username, db)
        flash("Deleted successfully")
    return redirect(url_for("blog.index"))


@bp.route("/<username>/messages", methods=("GET", "POST"))
@login_required
def messages(username):
    interactions = get_all_messages(g, username)
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
    count = get_visitor_count()
    return render_template("blog/account.html", username=username, visitor_count=count)
