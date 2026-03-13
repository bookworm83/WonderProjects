import pandas as pd
from typing import Optional, List, Tuple

class TableValidator:

      # Utility class for validating pandas DataFrames used as tables.

    @staticmethod
    def validate_primary_key(
        table: pd.DataFrame,
        id_column: str) -> None:

       # Ensures the primary key column exists, has no NULLs and no duplicates.

        if id_column not in table.columns:
            raise ValueError(f"Column '{id_column}' does not exist in table.")

        if table[id_column].isna().any():
            raise ValueError(
                f"Primary key column '{id_column}' contains NULL values."
            )

        if not table[id_column].is_unique:
            raise ValueError(
                f"Primary key column '{id_column}' contains duplicate values."
            )

    @staticmethod
    def validate_foreign_key(
            child_table: pd.DataFrame,
            child_column: str,
            parent_table: pd.DataFrame,
            parent_column: str
    ) -> None:

        # Ensures all values in child_column exist in parent_column of the parent table.

        if child_column not in child_table.columns:
            raise ValueError(f"Child column '{child_column}' does not exist in child table.")
        if parent_column not in parent_table.columns:
            raise ValueError(f"Parent column '{parent_column}' does not exist in parent table.")

        # This looks for each value in the child_column that does NOT exist in the parent_column
        missing_refs = ~child_table[child_column].isin(parent_table[parent_column])
        if missing_refs.any():
            invalid_values = child_table.loc[missing_refs, child_column].unique()
            raise ValueError(
                f"Foreign key constraint failed for column '{child_column}'. "
                f"Invalid values: {list(invalid_values)}"
            )

    @staticmethod
    def validate_required_columns(
            table: pd.DataFrame,
            required_columns: List[str]
    ) -> None:

        # Ensures required columns exist and contain no NULLs.

        missing_cols = [col for col in required_columns if col not in table.columns]
        if missing_cols:
            raise ValueError(f"Required columns missing from table: {missing_cols}")

        missing_vals = table[required_columns].isna().any()
        if missing_vals.any():
            raise ValueError(
                f"Missing values in required columns: {missing_vals[missing_vals].index.tolist()}"
                # Gives a list of the row indices where there are missing values.
            )

    @staticmethod
    def validate_no_duplicate_rows(table: pd.DataFrame) -> None:

        # Ensures the table has no duplicate rows.

        if table.duplicated().any():
            raise ValueError("Table contains duplicate rows.")

    @staticmethod
    def validate_table(
            table: pd.DataFrame,
            id_column: Optional[str] = None,
            foreign_keys: Optional[List[Tuple[str, pd.DataFrame, str]]] = None,
            required_columns: Optional[List[str]] = None
    ) -> None:
        """
        Runs all relevant validations in one call.

        Parameters:
        - id_column: name of the primary key column
        - foreign_keys: list of tuples (child_col, parent_table, parent_col)

        """

        if id_column is not None:
            TableValidator.validate_primary_key(table, id_column)

        TableValidator.validate_required_columns(table, required_columns)
        TableValidator.validate_no_duplicate_rows(table)

        if foreign_keys:
            for child_col, parent_table, parent_col in foreign_keys:
                TableValidator.validate_foreign_key(table, child_col, parent_table, parent_col)
