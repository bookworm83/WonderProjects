import sqlite3
import pandas as pd
from pathlib import Path

# Creates a stable path (absolute) based on the script location
base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir/'create_tables_in_db'/'pick_flick.db'

#### Classic Movies: Movies that came out in or before 2000,
## ordered by rate descending.
def get_classics():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')

    classic_movies = pd.read_sql_query('''
    SELECT 
        movie_title,
        release_year,
        runtime_min,
        genre
    FROM movies
    WHERE release_year <= 2000
    GROUP BY 1,2,3
    ORDER BY rate DESC;
    ''', conn)
    conn.close()

    classic_movies.index = classic_movies.index + 1

    return classic_movies

#### Hidden Gems: Movies with high ratings and in the bottom 30% of votes,
## ordered by rate descending.
def get_hidden_gems():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')

    gem_movies = pd.read_sql_query('''
    WITH percentile AS (
        SELECT votes
        FROM movies
        ORDER BY votes
        LIMIT 1 OFFSET CAST((SELECT COUNT(*) FROM movies) * 0.30 AS INTEGER)
        /* Skips the first 30% of the lowest votes, returning 1 row */
    )
    SELECT
        movie_title, 
        release_year, 
        runtime_min, 
        genre
    FROM movies 
    WHERE votes <= (SELECT votes FROM percentile)
    GROUP BY 1,2,3
    ORDER BY rate DESC;
    ''', conn)
    conn.close()

    gem_movies.index = gem_movies.index + 1

    return gem_movies

#### Masterpieces: Movies with a rate equal or greater than 8.5 and metascore >= 90
def get_masterpieces():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')

    masterpiece_movies = pd.read_sql_query('''
    SELECT 
        movie_title,
        release_year,
        runtime_min,
        genre
    FROM movies 
    WHERE rate >= 8.5 AND metascore >= 90
    GROUP BY 1,2,3
    ORDER BY votes DESC;
    ''', conn)
    conn.close()

    masterpiece_movies.index = masterpiece_movies.index + 1

    return masterpiece_movies

#### Popular and Short: Movies with a runtime of 100 minutes or less
## in the top 30% of votes, ordered by rate descending.
def get_short_popular():

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    popular_short_movies = pd.read_sql_query('''
    WITH percentile AS (
        SELECT votes
        FROM movies
        ORDER BY votes 
        LIMIT 1 OFFSET CAST((SELECT COUNT(*) FROM movies) * 0.70 AS INTEGER)
        /* Skips the first 70% of the lowest votes, returning 1 row */
    )
    SELECT
        movie_title,
        release_year,
        runtime_min,
        genre
    FROM movies 
    WHERE runtime_min <= 100
      AND votes >= (SELECT votes FROM percentile)
    GROUP BY 1,2,3
    ORDER BY rate DESC;
    ''', conn)
    conn.close()

    popular_short_movies.index = popular_short_movies.index + 1

    return popular_short_movies

#### Recent Movies: Movies that came out in or after 2010,
## ordered by rate descending.
def get_recent():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')

    recent_movies = pd.read_sql_query('''
    SELECT 
        movie_title,
        release_year,
        runtime_min,
        genre
    FROM movies
    WHERE release_year >= 2010
    GROUP BY 1,2,3
    ORDER BY rate DESC;
    ''', conn)
    conn.close()

    recent_movies.index = recent_movies.index + 1

    return recent_movies


