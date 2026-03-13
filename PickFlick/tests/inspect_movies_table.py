import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

df = load_data("../table_split_validate/movies_table.csv")
df.info()
df.head()