from flaskr.db import get_db


def increment_visitor_count():
    db = get_db()
    db.execute("UPDATE visitors SET count = count + 1 WHERE id = 1")
    db.commit()


def get_visitor_count():
    db = get_db()
    count = db.execute("SELECT count FROM visitors WHERE id = 1").fetchone()[0]
    return count
