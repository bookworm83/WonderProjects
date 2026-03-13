import pandas as pd

class DataframeCleaner:

    @staticmethod
    def standardize_columns(movies_df: pd.DataFrame) -> pd.DataFrame:
        # This function creates a copy of the movies dataframe and
        # standardizes the column names: strips whitespace, lowercase, replaces spaces with
        # underscores, returning the resulting dataframe with the modified columns.
        movies_df_copy = movies_df.copy()
        movies_df_copy.columns = (
            movies_df_copy.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
        )
        return movies_df_copy


    @staticmethod
    def trim_text_columns(movies_df: pd.DataFrame) -> pd.DataFrame:
        # This function creates a copy of the movies dataframe and
        # trims whitespace from all string columns,
        # returning the resulting dataframe with the modified columns.
        movies_df_copy = movies_df.copy()
        text_cols = movies_df_copy.select_dtypes(include="object").columns
        for col in text_cols:
            movies_df_copy[col] = movies_df_copy[col].str.strip()
        return movies_df_copy


    @staticmethod
    def enforce_string_types(movies_df: pd.DataFrame) -> pd.DataFrame:
        # This function creates a copy of the movies dataframe and
        # converts all object columns to string type,
        # returning the resulting dataframe.
        movies_df_copy = movies_df.copy()
        text_cols = movies_df_copy.select_dtypes(include="object").columns
        movies_df_copy[text_cols] = movies_df_copy[text_cols].astype("string")
        return movies_df_copy




    def clean(self, raw_file_path: str = "imdb_top_1000_raw.csv") -> pd.DataFrame:
        """
        Executes the full cleaning pipeline on a raw CSV file.
        Each transformation step builds on the result of the previous one,
        producing a fully cleaned dataset that is then saved.

        :param raw_file_path: Path to the raw CSV file.
        :return: Cleaned DataFrame.
        """

        # Step 1: Read the CSV
        movies_df = pd.read_csv(raw_file_path)

        # Step 2: Apply transformations
        movies_df = self.standardize_columns(movies_df)
        movies_df = self.trim_text_columns(movies_df)
        movies_df = self.enforce_string_types(movies_df)

        # Step 3: Save the cleaned file
        final_path = f"cleaned_{raw_file_path}"
        final_path = final_path.removesuffix("_raw.csv") + ".csv"
        movies_df.to_csv(final_path, index=False)
        return movies_df
