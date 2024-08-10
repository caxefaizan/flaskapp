from flaskr.db import get_db
import sqlite3
import itertools
from flaskr.visitors import get_visitor_count
from werkzeug.exceptions import abort
from flask import request

def get_messages(userId, receiver, size, check_author=True) -> sqlite3.Row:
    messageSize = int(size) * 5
    messages = []
    messages.append(
        get_db()
        .execute(
            f"SELECT m.* FROM messages m WHERE (m.senderId = '{userId}') AND (m.recipientId = '{receiver}')"
            f" ORDER BY m.timeStamp DESC LIMIT {messageSize}"
        )
        .fetchmany(messageSize)
    )
    messages.append(
        get_db()
        .execute(
            f"SELECT m.* FROM messages m WHERE (m.senderId = '{receiver}') AND (m.recipientId = '{userId}')"
            f" ORDER BY m.timeStamp DESC LIMIT {messageSize}"
        )
        .fetchmany(messageSize)
    )
    messages = [item for row in messages for item in row]

    return messages


def get_all_messages(g, username, check_author=True) -> sqlite3.Row:
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

    return profile


def get_profiles(check_author=True) -> sqlite3.Row:
    db = get_db()
    profiles = db.execute(
        "SELECT c.*, r.presentAddress AS present_address, u.lastActivity as lastActivity, u.id, u.username"
        " FROM client c JOIN residence r ON c.token = r.token JOIN user u ON u.username = c.token"
        " ORDER BY lastActivity DESC"
    ).fetchall()
    return profiles


def createUpdateProfile(db, action, formData, username):
    values = (
        formData["clientGender"],
        formData["clientCast"],
        formData["clientOccupation"],
        formData["clientEducation"],
        int(formData["clientAge"]),
        float(formData["clientHeight"]),
        formData["clientComplexion"],
        username,
    )
    if action == "edit":
        query = f"UPDATE client SET clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ? WHERE token = ?"
    else:
        query = "INSERT INTO client clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ?, token = ?"
    db.execute(query, values)


def createUpdatePreference(db, action, formData, username):
    values = (
        formData["clientGender"],
        formData["clientCast"],
        formData["clientOccupation"],
        formData["clientEducation"],
        int(formData["clientAge"]),
        float(formData["clientHeight"]),
        formData["clientComplexion"],
        username,
    )
    if action == "edit":
        query = f"UPDATE client SET clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ? WHERE token = ?"
    else:
        query = "INSERT INTO preference clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ?, token = ?"
    db.execute(query, values)


def getProfileData(username):
    profile = get_values(username, "client")
    sibling = get_values(username, "sibling")
    parents = get_values(username, "parents")
    preference = get_values(username, "preference")
    lifestyle = get_values(username, "lifestyle")
    residence = get_values(username, "residence")

    return [profile, sibling, parents, preference, lifestyle, residence]


def createUpdateProfileData(username, formData, action):
    db = get_db()
    if action == "create":
        print(formData["clientGender"])
        db.execute(
            "INSERT INTO client (clientGender, token, clientCast, clientOccupation, clientEducation, clientAge, clientHeight, clientComplexion)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                formData["clientGender"],
                username,
                formData["clientCast"],
                formData["clientOccupation"],
                formData["clientEducation"],
                int(formData["clientAge"]),
                float(formData["clientHeight"]),
                formData["clientComplexion"],
            ),
        )
        db.execute(
            "INSERT INTO preference (preferenceGender, token, preferenceOccupation, preferenceEducation, preferenceAge, preferenceHeight, preferencecomplexion)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "Female" if formData["clientGender"] == "M" else "Male",
                username,
                formData["preferenceOccupation"],
                formData["preferenceEducation"],
                int(formData["preferenceAge"]),
                float(formData["preferenceHeight"]),
                formData["preferenceComplexion"],
            ),
        )
        db.execute(
            "INSERT INTO parents (token, fathersOccupation, mothersOccupation, mothersCast, otherRelations)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                username,
                formData["fathersOccupation"],
                formData["mothersOccupation"],
                formData["mothersCast"],
                formData["otherRelations"],
            ),
        )
        db.execute(
            "INSERT INTO lifestyle (token, smoking, prayers, religiousSect)"
            " VALUES (?, ?, ?, ?)",
            (
                username,
                formData["smoking"],
                formData["prayers"],
                formData["religiousSect"],
            ),
        )
        db.execute(
            "INSERT INTO residence (token, presentAddress, permanentAddress, oldAddress)"
            " VALUES (?, ?, ?, ?)",
            (
                username,
                formData["presentAddress"],
                formData["permanentAddress"],
                formData["oldAddress"],
            ),
        )
        db.execute(
            "INSERT INTO sibling (token, siblingGender, siblingOccupation, siblingSpouseCast, siblingSpouseOccupation)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                username,
                formData["siblingGender"],
                formData["siblingOccupation"],
                formData["siblingSpouseCast"],
                formData["siblingSpouseOccupation"],
            ),
        )
    else:
        db.execute(
            "UPDATE client SET clientGender = ?, clientCast = ?, clientOccupation = ?, clientEducation = ?, clientAge = ?, clientHeight = ?, clientComplexion = ?"
            f"WHERE token = '{username}'",
            (
                formData["clientGender"],
                formData["clientCast"],
                formData["clientOccupation"],
                formData["clientEducation"],
                int(formData["clientAge"]),
                float(formData["clientHeight"]),
                formData["clientComplexion"],
            ),
        )
        db.execute(
            "UPDATE preference SET preferenceGender = ?, preferenceOccupation = ?, preferenceEducation = ?, preferenceAge = ?, preferenceHeight = ?, preferencecomplexion = ?"
            f"WHERE token = '{username}'",
            (
                "Female" if formData["clientGender"] == "Male" else "Male",
                formData["preferenceOccupation"],
                formData["preferenceEducation"],
                int(formData["preferenceAge"]),
                float(formData["preferenceHeight"]),
                formData["preferenceComplexion"],
            ),
        )
        db.execute(
            "UPDATE parents SET fathersOccupation = ?, mothersOccupation = ?, mothersCast = ?, otherRelations = ?"
            f"WHERE token = '{username}'",
            (
                formData["fathersOccupation"],
                formData["mothersOccupation"],
                formData["mothersCast"],
                formData["otherRelations"],
            ),
        )
        db.execute(
            "UPDATE lifestyle SET smoking = ?, prayers = ?, religiousSect = ?"
            f"WHERE token = '{username}'",
            (
                formData["smoking"],
                formData["prayers"],
                formData["religiousSect"],
            ),
        )
        db.execute(
            "UPDATE residence SET presentAddress = ?, oldAddress = ?"
            f"WHERE token = '{username}'",
            (
                formData["presentAddress"],
                formData["oldAddress"],
            ),
        )
        db.execute(
            "UPDATE sibling SET siblingGender = ?, siblingOccupation = ?, siblingSpouseCast = ?, siblingSpouseOccupation = ?"
            f"WHERE token = '{username}'",
            (
                formData["siblingGender"],
                formData["siblingOccupation"],
                formData["siblingSpouseCast"],
                formData["siblingSpouseOccupation"],
            ),
        )
    db.commit()


def preRouteChecks(g, action, username):
    if action != "view":
        if g.user["username"] != username:
            abort(403, f"Unauthorized!")

    if (action == "delete" and request.method == "GET") or (action == "view" and request.method == "POST"):
        abort(405, f"Method not allowed!")

    count = get_visitor_count()
    profileData = getProfileData(username)

    return count, profileData

def deleteProfileData(username, db):
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