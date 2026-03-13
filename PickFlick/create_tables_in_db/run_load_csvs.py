from pathlib import Path
import sqlite3
from PickFlick.create_tables_in_db import load_csvs


db_path = Path("pick_flick.db")
movies_path = Path("../table_split_validate/movies_table.csv")
genres_path = Path("../table_split_validate/genres_table.csv")
movie_genre_path = Path("../table_split_validate/movie_genre_table.csv")

def main():
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")

        load_csvs.import_all(conn, movies_path, genres_path, movie_genre_path)

        conn.commit()
        print("Import finished.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
