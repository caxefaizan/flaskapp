from flaskr.db import get_db
import sqlite3
import itertools


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
    print(senders, receivers)
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
