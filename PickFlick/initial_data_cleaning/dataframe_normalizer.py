import pandas as pd
import numpy as np

class DataframeNormalizer:

    @staticmethod
    def split_title_and_year(movies_df: pd.DataFrame, title_col: str = "title") -> pd.DataFrame:
        # This function splits the 'title' column which has both the movie title and the release year info
        # 'title' column format: '1. The Shawshank Redemption (1994)'
        movies_df_copy = movies_df.copy()

        if title_col not in movies_df_copy.columns:
            raise ValueError(f"Column '{title_col}' not found")

        ## This splits the 'title' column into two columns: 'movie_title' and 'release_year'

        # This removes the ranking prefix, leaving the string that is after the first '. '.
        no_rank = movies_df_copy[title_col].str.split('. ', n=1).str[1]
        # This splits from the right at ' ('
        split_values = no_rank.str.rsplit(' (', n=1)
        # Extracts the movie title (the first element (index 0) from the split result)
        movies_df_copy['movie_title'] = split_values.str[0]
        # Extracts the release_year (second element (index 1) from the split result)
        movies_df_copy['release_year'] = split_values.str[1].str.replace(')', '')
        # Converts the 'release_year' column into an integer that accepts null values
        movies_df_copy['release_year'] = movies_df_copy['release_year'].astype('Int64')

        # This drops the initial 'title' column from the DataFrame directly
        movies_df_copy.drop(columns=title_col, inplace=True)
        return movies_df_copy

    @staticmethod
    def split_cast(movies_df: pd.DataFrame, title_col: str = "cast") -> pd.DataFrame:
        # This function splits the 'cast' column which has both director and actors info
        # 'cast' column format: 'Director: Frank Darabont | Stars: Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler'
        movies_df_copy = movies_df.copy()

        if title_col not in movies_df_copy.columns:
            raise ValueError(f"Column '{title_col}' not found")

        # This splits the 'cast' column into two columns: 'director' and 'actors'
        split_values = (movies_df_copy[title_col]
                        .str.replace('Director:', '', regex=False) # replaces the exact text
                        .str.rsplit('|', n=1) # it splits once starting from the right side
                        )
        movies_df_copy['director'] = split_values.str[0].str.strip()
        movies_df_copy['actors'] = (split_values.str[1]
                                    .str.replace('Stars:', '', regex=False).str.strip()
                                    )

        # This removes the initial 'cast' column
        movies_df_copy.drop(columns=title_col, inplace=True)
        return movies_df_copy

    @staticmethod
    def split_info(movies_df: pd.DataFrame, title_col: str = "info") -> pd.DataFrame:
        # This functions splits the 'info' column which has both votes and gross values
        # 'info' column format: 'Votes: 2,295,987 | Gross: $28.34M'
        movies_df_copy = movies_df.copy()

        if title_col not in movies_df_copy.columns:
            raise ValueError(f"Column '{title_col}' not found")

        # This splits the 'info' column into 'votes' and gross_usd'
        split_values = (movies_df_copy[title_col]
                        .str.replace('Votes:', '', regex=False).str.rsplit('|', n=1)
                        )
        movies_df_copy['votes'] = (split_values.str[0]
                                   .str.replace(',', '', regex=False)
                                   .str.strip()
                                   .astype('Int64')
                                   )
        movies_df_copy['gross_usd'] = (split_values.str[1]
                                       .str.replace('Gross: $', '', regex=False)
                                       .str.replace('M', '', regex=False)
                                       .astype(float)
                                       .mul(1_000_000)
                                       .apply(np.floor)
                                       .astype('Int64')
                                       )

        movies_df_copy.drop(columns=[title_col], inplace=True)
        return movies_df_copy

    @staticmethod
    def tidy_runtime(movies_df: pd.DataFrame, title_col: str = "duration") -> pd.DataFrame:
        # 'duration' column format: '142 min'
        movies_df_copy = movies_df.copy()

        if title_col not in movies_df_copy.columns:
            raise ValueError(f"Column '{title_col}' not found")

        movies_df_copy['runtime_min'] = (movies_df_copy[title_col].str.replace('min', '', regex=False)
                                         .str.strip()
                                         .astype("Int64"))

        movies_df_copy.drop(columns=title_col, inplace=True)
        return movies_df_copy

    @staticmethod
    def check_duplicate_rows(movies_df: pd.DataFrame):
        duplicates = movies_df[movies_df.duplicated(keep=False)]
        if duplicates.empty:
            print('No duplicate rows found in dataframe.')
            return
        print('Duplicate rows detected:')
        print(duplicates)

    def normalize(self, raw_file_path: str = "cleaned_imdb_top_1000.csv") -> pd.DataFrame:
        """
        Executes the full normalizing pipeline on a raw CSV file.
        Each transformation step builds on the result of the previous one,
        producing a fully normalized dataset that is then saved.

        :param raw_file_path: Path to the raw CSV file.
        :return: Normalized DataFrame.
        """

        # Step 1: Read the CSV
        movies_df = pd.read_csv(raw_file_path)

        # Step 2: Apply transformations
        movies_df = self.split_title_and_year(movies_df)
        movies_df = self.split_cast(movies_df)
        movies_df = self.split_info(movies_df)
        movies_df = self.tidy_runtime(movies_df)
        self.check_duplicate_rows(movies_df)

        # Step 3: Save the normalized file
        final_path = f"{raw_file_path}"
        final_path = final_path.removeprefix("cleaned")
        final_path = 'normalized' + final_path
        movies_df.to_csv(final_path, index=False)

        return movies_df


