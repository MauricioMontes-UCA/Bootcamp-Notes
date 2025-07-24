import pandas as pd

# Carga de datos
dataset = pd.read_csv('flight-price.csv')

# El dataset es tan limpio que esto no es realmente necesario
dataset.drop_duplicates()
dataset.dropna()

# Drop de columnas innecesarias
dataset = dataset.drop(columns=['Unnamed: 0', 'flight'])