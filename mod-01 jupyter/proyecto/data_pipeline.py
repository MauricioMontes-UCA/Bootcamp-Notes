import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Carga de datos
df = pd.read_csv("flight-price.csv")

# Limpieza básica
df.drop_duplicates(); 
df.dropna(); 

# Eliminando columnas innecesarias
df.drop(columns=['flight', 'Unnamed: 0'], inplace=True); 

# Nueva columna
df['route'] = df['source_city'] + ' to ' + df['destination_city']

# Segmentación por clase de vuelo
df_economy = df[df['class'] == 'Economy']
df_business = df[df['class'] != 'Economy']