-- Drop fifa18 table
DROP TABLE fifa18;

-- Truncate fifa18 table
TRUNCATE TABLE fifa18;

-- DDL for fifa18 table
CREATE TABLE fifa18
(
  names     CHAR(30) CHARACTER SET latin1 COLLATE latin1_bin,
  club      varchar(30) ,
  league    varchar(30),
  position  varchar(30),
  rating    INTEGER(2),
  pace      INTEGER(2),
  shooting  INTEGER(2),
  passing   INTEGER(2),
  dribbling INTEGER(22),
  defending INTEGER(22),
  physical  INTEGER(22),
  loaddate  timestamp
);

-- Insert statement example
INSERT INTO futhead.fifa18 (names, club, league, position, rating, pace, shooting, passing, dribbling, defending, physical, loaddate) VALUES ("Alexander Esswein", "Hertha Berlin", "Bundesliga", "RM", 73, 89, 72, 65, 72, 31, 75, NOW());