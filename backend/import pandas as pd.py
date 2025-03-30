import pandas as pd
import pathlib as pl

data = pl.Path(__file__).parent.absolute() / 'data'
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

print(dict(associations_df[associations_df['id'] == id]))