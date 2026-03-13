import unittest
import pandas as pd
from PickFlick.table_split_validate.table_validator import TableValidator

class TestTableValidator(unittest.TestCase):
    def test_validate_primary_key_ok(self):
        df = pd.DataFrame({'id': [1, 2, 3], 'val': ['a', 'b', 'c']})
        # should not raise
        TableValidator.validate_primary_key(df, 'id')

    def test_validate_primary_key_missing_column(self):
        df = pd.DataFrame({'val': [1, 2, 3]})
        with self.assertRaises(ValueError) as cm:
            TableValidator.validate_primary_key(df, 'id')
        self.assertIn("does not exist", str(cm.exception))

    def test_validate_primary_key_null(self):
        df = pd.DataFrame({'id': [1, None, 3]})
        with self.assertRaises(ValueError) as cm:
            TableValidator.validate_primary_key(df, 'id')
        self.assertIn("contains NULL", str(cm.exception))

    def test_validate_primary_key_duplicates(self):
        df = pd.DataFrame({'id': [1, 2, 2]})
        with self.assertRaises(ValueError) as cm:
            TableValidator.validate_primary_key(df, 'id')
        self.assertIn("duplicate", str(cm.exception).lower())

    def test_validate_foreign_key_ok(self):
        parent = pd.DataFrame({'id': [10, 20, 30]})
        child = pd.DataFrame({'fk': [10, 20]})
        TableValidator.validate_foreign_key(child, 'fk', parent, 'id')

    def test_validate_foreign_key_invalid(self):
        parent = pd.DataFrame({'id': [10, 20]})
        child = pd.DataFrame({'fk': [10, 99]})
        with self.assertRaises(ValueError) as cm:
            TableValidator.validate_foreign_key(child, 'fk', parent, 'id')
        self.assertIn('Invalid values', str(cm.exception))
        self.assertIn('99', str(cm.exception))

    def test_validate_no_missing_values_ok(self):
        df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        TableValidator.validate_no_missing_values(df)

    def test_validate_no_missing_values_fail(self):
        df = pd.DataFrame({'a': [1, None], 'b': ['x', 'y']})
        with self.assertRaises(ValueError) as cm:
            TableValidator.validate_no_missing_values(df)
        self.assertIn('missing values', str(cm.exception))

    def test_validate_no_duplicate_rows_ok(self):
        df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        TableValidator.validate_no_duplicate_rows(df)

    def test_validate_no_duplicate_rows_fail(self):
        df = pd.DataFrame({'a': [1, 1], 'b': ['x', 'x']})
        with self.assertRaises(ValueError):
            TableValidator.validate_no_duplicate_rows(df)

    def test_validate_table_combined_ok(self):
        parent = pd.DataFrame({'id': [1, 2]})
        child = pd.DataFrame({'id': [10, 11], 'parent_id': [1, 2]})
        TableValidator.validate_table(child, id_column='id', foreign_keys=[('parent_id', parent, 'id')])

    def test_validate_table_foreign_key_fail(self):
        parent = pd.DataFrame({'id': [1]})
        child = pd.DataFrame({'id': [10], 'parent_id': [99]})
        with self.assertRaises(ValueError):
            TableValidator.validate_table(child, id_column='id', foreign_keys=[('parent_id', parent, 'id')])

if __name__ == '__main__':
    unittest.main()
