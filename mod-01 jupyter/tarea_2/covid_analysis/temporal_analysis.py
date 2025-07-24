import pandas as pd
import plotly.express as plt

# Carga de los datos
df = pd.read_csv("time_series_covid19_confirmed_global.csv")

# Transformación de los datos...

# Pasando las columnas fecha a una columna, y los datos de casos confirmados a una columna
df = df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
    var_name='Date', 
    value_name='Confirmed'
)

# Ahora, todas las fechas se pasan al formato datetime
df['Date'] = pd.to_datetime(df['Date'])
df['YearMonth'] = df['Date'].dt.to_period('M') # Nueva columna mes-año para poder agrupar

# Los casos confirmados son acumulados, no son nuevos casos por día; es por eso que se obtiene el máximo por mes.
df = df.groupby(['Country/Region', 'YearMonth'])['Confirmed'].max().reset_index()
# Para obtener nuevos casos por mes, hay que hacer una diferencia de los casos confirmados de un mes con el anterior
df['NewCases'] = df.groupby(['Country/Region'])['Confirmed'].diff().fillna(0)

# Seleccionando países para análisis de datos
countries = ['US', 'United Kingdom', 'El Salvador']
subset = df[df['Country/Region'].isin(countries)]

# Visualización de datos
subset['YearMonth'] = subset['YearMonth'].dt.to_timestamp() # Transformación necesaria para plotly

fig = plt.line(
    subset,
    x = 'YearMonth',
    y = 'NewCases',
    color = 'Country/Region',
    title = 'Nuevos casos confirmados por mes'
)

fig.update_layout(
    xaxis_title = 'Fecha',
    yaxis_title = 'Casos confirmados',
    hovermode = 'x unified'
)

fig.show()