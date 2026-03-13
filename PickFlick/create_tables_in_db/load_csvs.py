from pathlib import Path
import sqlite3
import pandas as pd


def load_csv_into_table(conn: sqlite3.Connection, csv_path: Path, table: str) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f'CSV not found: {csv_path}')

    table_df = pd.read_csv(csv_path)

    if table_df.empty:
        print(f'{csv_path} is empty.')
        return

    cols = list(table_df.columns)

    placeholders = ','.join('?' for _ in cols) # loop once per column, without using the value
    # They represent slots for values that will be replaced with the actual values at execution time
    # format is (?,?,?, ...), '?' for every column in the table

    col_list = ','.join(f'"{c}"' for c in cols)
    sql = f'INSERT INTO "{table}" ({col_list}) VALUES ({placeholders})'

    rows = [
        tuple(None if pd.isna(x) else x for x in row)
        for row in table_df.itertuples(index=False, name=None) # converts rows into tuples
    ]
    cur = conn.cursor()
    cur.executemany(sql, rows)
    cur.close()

    print(f'Inserted {len(table_df)} rows into "{table}".')


def import_all(conn: sqlite3.Connection, movies_path, genres_path, movie_genre_path):
    load_csv_into_table(conn, movies_path, 'movies')
    load_csv_into_table(conn, genres_path, 'genres')
    load_csv_into_table(conn, movie_genre_path, 'movie_genre')



