import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path


@st.cache_resource # the connection is created once and is reused
def get_connection():
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir/'create_tables_in_db'/'pick_flick.db'
    conn = sqlite3.connect(db_path, check_same_thread=False) # allows the connection to be reused safely by streamlit
    conn.execute('PRAGMA foreign_keys = ON')  # enables foreign key constrains
    return conn

def movie_picker(ctg_df, movie_ctg, display_name):
    title_col = 'movie_title'
    year_col = 'release_year'
    runtime_col = 'runtime_min'
    genre_col = 'genre'

    #unique names for the session state variables
    list_key = f'{movie_ctg}_list'
    index_key = f'{movie_ctg}_index'

    if st.button(f'Pick {display_name}'):
        if list_key not in st.session_state: # 'st.session_state' saves information that is kept between script reruns
            st.session_state[list_key] = ctg_df.sample(frac=1).reset_index(drop=True) # 'sample(frac=1)' randomly shuffles the df
            st.session_state[index_key] = 0 # start with the first movie in the shuffled list

        # Retrieve stored values
        index = st.session_state[index_key]
        movie_list = st.session_state[list_key]

        if index >= len(movie_list):
            # the code reshuffles again
            st.session_state[list_key] = ctg_df.sample(frac=1).reset_index(drop=True)
            st.session_state[index_key] = 0
            # then reloads
            movie_list = st.session_state[list_key]
            index = 0

        # selects the movie by position
        movie = movie_list.iloc[index]

        # displays the movie with its details
        st.subheader(movie[title_col])
        st.write(f'Release year: {movie[year_col]}')
        st.write(f'Runtime: {movie[runtime_col]}')
        st.write(f'Genre: {movie[genre_col]}')

        # moves to the next movie
        st.session_state[index_key] += 1

def get_movies_by_genre(genre_name):
    conn = get_connection()

    query = '''
    SELECT DISTINCT
        m.movie_title,
        m.release_year,
        m.runtime_min, 
        m.genre
    FROM movies m
    JOIN movie_genre mg ON m.movie_id = mg.movie_id
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE g.genre_name = ?
    
    '''
    return pd.read_sql_query(query, conn, params = [genre_name]) # params supplies values for SQL placeholders (?)

def get_genre_list():
    conn = get_connection()
    query = '''
    SELECT genre_name FROM genres
    ORDER BY genre_name;
    '''
    return pd.read_sql(query, conn)['genre_name'].tolist() # returns the genre_name column contents as a list