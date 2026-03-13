import pandas as pd
import sqlite3

conn = sqlite3.connect("../create_tables_in_db/pick_flick.db")
conn.execute("PRAGMA foreign_keys = ON")

df = pd.read_sql_query('''
SELECT COUNT(*) FROM movie_genre;
''', conn)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df)
conn.close()
