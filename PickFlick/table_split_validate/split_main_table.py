import pandas as pd
from pathlib import Path
from typing import List

def ensure_int_columns(csv_path: str, int_columns: List[str] = None) -> pd.DataFrame:
    path = Path(csv_path)
    if int_columns is None:
        int_columns = []

    # Create dtype dictionary for pandas
    dtype_dict = {col: "Int64" for col in int_columns}

    # Read CSV with dtype applied on the columns listed in int_columns
    movies_df = pd.read_csv(path, dtype=dtype_dict)
    return movies_df

def check_required_columns(movies_df: pd.DataFrame, required: List[str]) -> None:
    missing_cols = [c for c in required if c not in movies_df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")


def create_movies_table(movies_df: pd.DataFrame) -> pd.DataFrame:
    required = [
        'movie_title',
        'release_year',
        'runtime_min',
        'genre',
        'rate',
        'metascore',
        'votes',
        'director',
        'gross_usd'
    ]
    check_required_columns(movies_df, required)
    movies_table = movies_df[required].copy()
    movies_table = movies_table.reset_index(drop=True) # resets the index, drops the old index column
    movies_table.insert(0, "movie_id", movies_table.index + 1)

    return movies_table


def create_genres_table(movies_df: pd.DataFrame) -> pd.DataFrame:
    check_required_columns(movies_df, ["genre"])
    genres_series = (
        movies_df["genre"]
        .str.split(",")
        .explode() # turns each list element into its own row.
        .str.strip()
        .dropna()
    )

    genres_table = (
        genres_series
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
        .to_frame(name="genre_name") # converts the series object to a dataframe
    )

    genres_table.insert(0, "genre_id", genres_table.index + 1)
    return genres_table

def create_movie_genre_table(
    movies_table: pd.DataFrame,
    genres_table: pd.DataFrame,
    movies_df: pd.DataFrame
) -> pd.DataFrame:

    check_required_columns(movies_df, ["movie_title", "genre"])
    movie_genre_table = (
        movies_df[["movie_title", "genre"]]
        .assign(genre=lambda x: x["genre"].str.split(",")) # modifies the 'genre' column mid-chain without breaking the pipeline into separate steps.
        .explode("genre")
    )

    movie_genre_table["genre"] = movie_genre_table["genre"].str.strip()

    movie_genre_table = movie_genre_table.merge(
        movies_table[["movie_id", "movie_title"]],
        on="movie_title",
        how="left" # left join, keeps all rows from movie_genre_table, bringing matching 'movie_id' from movies_table
    )

    movie_genre_table = movie_genre_table.merge(
        genres_table,
        left_on="genre", # column in movie_genre_table
        right_on="genre_name", # column in genres_table
        how="left"
    )

    movie_genre_table = movie_genre_table.drop_duplicates().reset_index(drop=True)

    return movie_genre_table[["movie_id", "genre_id"]]

def save_table(table: pd.DataFrame, filename: str) -> None:
    path = Path(filename)
    if path.suffix.lower() != ".csv":
        path = path.with_suffix(".csv")
    table.to_csv(path, index=False)

