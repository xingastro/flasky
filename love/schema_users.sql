DROP TABLE IF EXISTS users;
CREATE TABLE users (
  name     CHAR NOT NULL PRIMARY KEY,
  password CHAR NOT NULL,
  sex      CHAR NOT NULL,
  info     TEXT
);