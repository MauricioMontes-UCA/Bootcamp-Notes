# autor: Mauricio Montes
# fecha: 15 jun 2025
# descripción: Clases para poder realizar procesamiento y análisis de datos

import pandas as pd

# ====================================================================================================

class DataPreprocessor:
    """
    Clase por medio de la cual se procesan de manera sencilla los datos usando métodos de
    `pandas`.

    Atributos:
        dataframe (pandas.DataFrame | None): Es el atributo que guarda los datos cargados.
    """

    def __init__(self) -> None:
        self._dataframe: pd.DataFrame | None = None

    def cargar_datos(self, path: str, separator: str = ",", start_row: int = 1) -> None:
        """
        Carga los datos a partir de un archivo .csv

        Args:
            path (str): Cadena de texto con la ruta del archivo `.csv`.
            separator (str): Carácter o cadena para separar los datos. Por defecto ",".
            start_row (int): Fila por la que se empieza la carga de datos, empezando desde 1 como primera fila.

        Returns:
            `None`

        Raises:
            TypeError: Si `path` o `separator` no son cadenas de texto, o si `start_row` no es un entero.
        """

        if not isinstance(path, str):
            raise TypeError(f"Argumento 'path' esperaba un str, pero se dió un {type(path)}")
        elif not isinstance(separator, str):
            raise TypeError(f"Argumento 'separator' esperaba un str, pero se dió un {type(separator)}")
        elif not isinstance(start_row, int):
            raise TypeError(f"Argumento 'separator' esperaba un str, pero se dió un {type(separator)}")

        self._dataframe = pd.read_csv(
            filepath_or_buffer= path,
            sep= separator,
            skiprows= start_row-1 # para considerar el índice cero
        )
    
    def _validar_dataframe(self) -> pd.DataFrame:
        """
        Valida si `dataframe` es `None` o algún otro tipo de dato que no sea `pandas.DataFrame`.
        Es una clase privada, no se supone que se use fuera de la clase.

        Returns:
            `pandas.DataFrame`
        
        Raises:
            ValueError: Si `dataframe` es `None`.
            TypeError: Si `dataframe` no es un objeto de `pandas.DataFrame`.
        """

        if self._dataframe is None:
            raise ValueError("El atributo dataframe no tiene asignado ningún DataFrame a él.")
        elif not isinstance(self._dataframe, pd.DataFrame):
            raise TypeError("El atributo dataframe (de alguna forma) no guarda un valor DataFrame.")
        return self._dataframe


    def limpiar_datos(self) -> None:
        """
        Realiza una validación con `_validar_dataframe()`, para después eliminar duplicados y registros con 
        valores nulos.

        Returns:
            `None`.

        Raises:
            ValueError, TypeError: Dependiendo de la validación de `_validar_dataframe()`.
        """

        df = self._validar_dataframe()
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        
    def exportar_datos(self, path:str) -> None:
        """
        Exporta los datos contenidos en `dataframe` en un archivo .csv

        Returns:
            `None`.

        Raises:
            TypeError: Si `path` no es una cadena.
            ValueError, TypeError: Dependiendo de la validación de `_validar_dataframe()`.
        """

        if not isinstance(path, str):
            raise TypeError(f"Argumento 'path' esperaba un str, pero se dió un {type(path)}")

        df = self._validar_dataframe()
        df.to_csv(
            path_or_buf= path,
            index= False,           # no cuenta a los índices como serie
            encoding= 'utf-8'       # soporta caracteres unicode
        )

    @property
    def dataframe(self) -> pd.DataFrame:
        """
        Es un getter de `dataframe` realmente, con la validación de que no es nulo u otro tipo de dato.

        Returns:
            `pandas.DataFrame`
        
        Raises:
            ValueError, TypeError: Dependiendo de la validación de `_validar_dataframe()`.
        """
        df = self._validar_dataframe()
        return df
    
    @dataframe.setter
    def dataframe(self, df: pd.DataFrame):
        self._dataframe = df

# ====================================================================================================

class DataAnalyzer(DataPreprocessor):
    """
    Clase para realizar análisis de datos, heredando de `DataPreprocessor` para tener
    acceso a los métodos de limpieza y procesamiento de datos.
    """
    def __init__(self) -> None:
        super().__init__()

    def resumen(self) -> pd.DataFrame:
        """
        Devuelve los máximos, mínimos y medias de las series numéricas de los datos guardados
        en el atributo `dataframe`; después de validar usando `_validar_dataframe()`.

        Returns:
            `pandas.DataFrame`

        Raises:
            ValueError, TypeError: Dependiendo de la validación de `_validar_dataframe()`.
        """
        df = self._validar_dataframe()

        return pd.DataFrame({
            'max': df.max(numeric_only=True),
            'min': df.min(numeric_only=True),
            'media': df.mean(numeric_only=True)
        }).transpose()  
        # el dataframe tiene como columnas max, min & mean; pero quiero que esas sean las filas
        # por eso el transpose(), para transponer la tabla y que se vea similar a describe()