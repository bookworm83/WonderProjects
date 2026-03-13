from PickFlick.table_split_validate.split_main_table import (
    ensure_int_columns,
    create_movies_table,
    create_genres_table,
    create_movie_genre_table,
    save_table
)

def main() -> None:
    csv_path = '../initial_data_cleaning/normalized_imdb_top_1000.csv'
    int_columns = ['metascore', 'gross_usd', 'votes']
    try:
        movies_df = ensure_int_columns(str(csv_path), int_columns)
    except FileNotFoundError as e:
        print(e)
        return

    movies_table = create_movies_table(movies_df)
    genres_table = create_genres_table(movies_df)
    movie_genre_table = create_movie_genre_table(movies_table, genres_table, movies_df)

    save_table(movies_table, 'movies_table.csv')
    save_table(genres_table, 'genres_table.csv')
    save_table(movie_genre_table, 'movie_genre_table.csv')

if __name__ == '__main__':
    main()
