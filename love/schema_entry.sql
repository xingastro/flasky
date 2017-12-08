DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  content      TEXT    NOT NULL,
  birthday     DATE,
  good_counter INT                 DEFAULT 0,
  master       TEXT    NOT NULL REFERENCES users (name),
  towho        INTEGER NOT NULL REFERENCES moods (id),
  sex          TEXT    NOT NULL
);