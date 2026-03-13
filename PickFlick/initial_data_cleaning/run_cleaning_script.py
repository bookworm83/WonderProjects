from dataframe_cleaner import DataframeCleaner
from dataframe_normalizer import DataframeNormalizer
import pandas as pd

cleaner = DataframeCleaner()
cleaner.clean("imdb_top_1000_raw.csv")

normalizer = DataframeNormalizer()
normalizer.normalize("cleaned_imdb_top_1000.csv")

#DataframeNormalizer().check_duplicate_rows(pd.read_csv('normalized_imdb_top_1000.csv'))