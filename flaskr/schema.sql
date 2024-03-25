PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS lifestyle;
DROP TABLE IF EXISTS parents;
DROP TABLE IF EXISTS residence;
DROP TABLE IF EXISTS sibling;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS client (
    token TEXT NOT NULL UNIQUE PRIMARY KEY,
    clientCast TEXT NOT NULL,
    occupation TEXT NOT NULL,
    education TEXT NOT NULL,
    age INTEGER NOT NULL,
    height FLOAT NOT NULL,
    complexion TEXT NOT NULL,
    preferenceToken TEXT,
    clientType TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sibling (
    id INTEGER UNIQUE PRIMARY KEY,
    relatedToken TEXT NOT NULL,
    sex TEXT NOT NULL,
    occupation TEXT NOT NULL,
    spouseCast TEXT NOT NULL,
    spouseOccupation TEXT NOT NULL,
    FOREIGN KEY (relatedToken) REFERENCES client(token)
);

CREATE TABLE IF NOT EXISTS parents (
    id INTEGER UNIQUE PRIMARY KEY,
    relatedToken TEXT NOT NULL,
    fathersOccupation TEXT NOT NULL,
    mothersOccupation TEXT NOT NULL,
    mothersCast TEXT NOT NULL,
    FOREIGN KEY (relatedToken) REFERENCES client(token)
);

CREATE TABLE IF NOT EXISTS lifestyle (
    id INTEGER UNIQUE PRIMARY KEY,
    relatedToken TEXT NOT NULL,
    smoking TEXT NOT NULL,
    prayers TEXT NOT NULL,
    religiousSect TEXT NOT NULL,
    FOREIGN KEY (relatedToken) REFERENCES client(token)
);

CREATE TABLE IF NOT EXISTS residence (
    id INTEGER UNIQUE PRIMARY KEY,
    relatedToken TEXT NOT NULL,
    presentAddress TEXT NOT NULL,
    oldAddress TEXT NOT NULL,
    FOREIGN KEY (relatedToken) REFERENCES client(token)
);