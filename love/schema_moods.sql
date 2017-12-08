DROP TABLE IF EXISTS moods;
CREATE TABLE moods (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  content        TEXT NOT NULL,
  birthday       DATE,
  browse_counter INT                 DEFAULT 0,
  good_counter   INT                 DEFAULT 0,
  bgcolor        TEXT                DEFAULT "white",
  master         TEXT NOT NULL REFERENCES users (name),
  master_sex     TEXT NOT NULL
);