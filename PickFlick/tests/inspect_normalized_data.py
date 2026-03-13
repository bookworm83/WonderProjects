import pandas as pd

def load_raw_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

df = load_raw_data("../initial_data_cleaning/normalized_imdb_top_1000.csv")
df.info()
df.head()