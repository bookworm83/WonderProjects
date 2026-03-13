from table_validator import TableValidator
import pandas as pd


movies_df = pd.read_csv('movies_table.csv')
genres_df = pd.read_csv('genres_table.csv')
movie_genre_df = pd.read_csv('movie_genre_table.csv')

TableValidator.validate_table(movies_df, id_column='movie_id', required_columns=['movie_title', 'release_year'])
TableValidator.validate_table(genres_df, id_column='genre_id', required_columns=['genre_name'])
TableValidator.validate_table(movie_genre_df, id_column=None,
                              foreign_keys=[('movie_id', movies_df, 'movie_id'),
                                            ('genre_id', genres_df, 'genre_id')],
                              required_columns=['movie_id', 'genre_id'])
