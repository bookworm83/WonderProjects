import streamlit as st
from typing import Literal
from what_to_watch.define_categories import (get_classics, get_hidden_gems, get_masterpieces, get_short_popular, get_recent)
from what_to_watch.pick_a_movie import (get_connection, movie_picker, get_movies_by_genre, get_genre_list)


st.set_page_config(page_title='PickFlick', layout='wide')

st.title('PickFlick')
st.write('Stop scrolling. Start watching.')

st.markdown('''
<style>

div.stButton button p {        /* targets the paragraph (p) element inside the button */
font-size: 14px !important;    /* forces this rule to override any other CSS rules */
}

/* normal genre buttons */
div.stButton > button {         /* styles only the immediate button, not deeper nested elements */
border: 1px solid #5b5b5b;
color: #ffffff;                 /* text colour */
background-color: transparent;  /* this removes the default button background */
border-radius: 25px;            /* rounds the corners of the button */
}

/* selected button primary */
div.stButton > button[kind = 'primary'] {  
background-color: #000000;
color: #27ff00;
border: 1px solid #27ff00;
}
</style>
''', unsafe_allow_html=True) # allows raw HTML to be rendered instead of being treated as plain text

conn = get_connection()

category_map = {
    'Classics': ('classic', get_classics, 'classic flick'),
    'Hidden Gems': ('hidden_gem', get_hidden_gems, 'hidden gem'),
    'Masterpieces': ('masterpiece', get_masterpieces,'masterpiece'),
    'Short and Popular': ('short_popular', get_short_popular, 'short & popular flick'),
    'Recents': ('recent', get_recent, 'recent flick')
}

category = st.pills('Categories:', list(category_map.keys()),
                    label_visibility='hidden')

if category:
    ctg_key, func, display = category_map[category]
    ctg_df = func()
    movie_picker(ctg_df, ctg_key, display)
    if st.button(f'See all {category}'):
        st.dataframe(ctg_df)

st.write(' ')

genre_list = get_genre_list()

genres_per_row = 7

# creates rows of lists (7 genres each)
rows = [genre_list[i:i+genres_per_row] for i in range (0, len(genre_list), genres_per_row)]


if 'genre_choice' not in st.session_state:
    # creates the key 'genre_choice' if it does not exist in the session_state (which behaves like a dict)
    st.session_state.genre_choice = None

for row in rows:
    cols = st.columns(len(row))
    for col, genre in zip(cols, row): # each genre gets its own column
        with col:
            # checks whether the genre is currently selected
            button_type: Literal['primary', 'secondary'] = (
                'primary' if genre == st.session_state.genre_choice else 'secondary')
            # each button has a unique key that prevents st conflicts
            if st.button(genre, key=f'genre_{genre}', width = 140, type = button_type):
                st.session_state.genre_choice = genre # stores the selected genre
                st.rerun() # st reruns the script, the selected button visually updates right away

# retrieves the chosen genre
genre_choice: str|None = st.session_state.genre_choice

if genre_choice is not None: # runs only if the user clicked a genre button
    genre_df = get_movies_by_genre(genre_choice)

    movie_picker(genre_df, genre_choice.lower().replace(' ', '_'),
                 (genre_choice.lower() + ' flick'))
    if st.button(f'See all {genre_choice} flicks'):
        genre_df.index = genre_df.index + 1
        st.dataframe(genre_df)



#### Check for duplicates in dataframe:
# duplicates = df[df.duplicated(keep=False)] # marks all occurrences of duplicated rows as True.
# if duplicates.empty:
#     st.success('No duplicate rows found.')
# else:
#     st.error('Duplicate rows detected.')
#     st.dataframe(duplicates)