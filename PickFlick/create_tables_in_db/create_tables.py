import sqlite3

conn = sqlite3.connect("pick_flick.db")
conn.execute("PRAGMA foreign_keys = ON") # Enforces foreign key rules in sqlite

conn.executescript("""
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    movie_title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    runtime_min INTEGER,
    genre TEXT,
    rate REAL,
    metascore INTEGER,
    votes INTEGER,
    director TEXT,
    gross_usd INTEGER
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE, 
    /* If a row in movies is deleted, it automatically deletes all related rows in the child table */
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);
""")

conn.close()