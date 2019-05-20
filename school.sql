DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS teachers;

CREATE TABLE students (
  studentid INTEGER PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);

CREATE TABLE quizzes (
  quizid INTEGER PRIMARY KEY,
  subject TEXT NOT NULL,
  questions INTEGER NOT NULL,
  date TEXT NOT NULL
);

CREATE TABLE grades (
  studentid INTEGER NOT NULL,
  quizid INTEGER NOT NULL,
  score INTEGER NOT NULL,
  FOREIGN KEY (studentid) REFERENCES students(studentid),
  FOREIGN KEY (quizid) REFERENCES quizzes(quizid)
);

CREATE TABLE teachers (
  teacherid INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT,
  lastname TEXT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
)