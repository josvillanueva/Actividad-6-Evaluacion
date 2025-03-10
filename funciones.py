####Leer  data frames (xlsx) y (csv)
def leer_dataframe(archivo):
    import pandas as pd
    import os
    extension = os.path.splitext(archivo)[1].lower() 
    if extension ==".csv":
        df=pd.read_csv(archivo)
        return(df)
    elif extension ==".xlsx":
        df=pd.read_excel(archivo)
        return(df)
    else:
        raise ValueError(f"Formato de archivo no soportado{extension}")


#####Sustituir valores nulos de las columnas numericas pares con mean##
def sustituir_valores_nulos(dataframe):
    import pandas as pd
    columnas_pares_con_nulos = dataframe.iloc[:, ::2]  
    numericas = columnas_pares_con_nulos.select_dtypes(include=["float64","int64","float","int"])
    no_numericas = columnas_pares_con_nulos.select_dtypes(include=["object","datetime","category"])   
    filas_pares = numericas.fillna(round(numericas.mean(), 1))
    no_numericas = no_numericas.fillna("Este es un valor nulo")
    filas_pares_sin_nulos = pd.concat([filas_pares, no_numericas],axis=1)

    columnas_impares_con_nulos = dataframe.iloc[:, 1::2]
    numericas_impares = columnas_impares_con_nulos.select_dtypes(include=["float64","int64","float","int"])
    no_numericas_impares  = columnas_impares_con_nulos.select_dtypes(include=["object","datetime","category"])
    filas_impares = numericas_impares.fillna(99)
    no_numericas_impares = no_numericas_impares.fillna("Este es un valor nulo")
    filas_impares_sin_nulos = pd.concat([filas_impares, no_numericas_impares], axis=1)
    dataframe_sin_nulos = pd.concat([filas_pares_sin_nulos,filas_impares_sin_nulos], axis=1)
    return dataframe_sin_nulos

### Función_3. Identifica los valores nulos “por columna” y “por dataframe”
def identificar_nulos(dataframe):
    import pandas as pd
    #por columna
    valores_nulos_cols = dataframe.isnull().sum()
    #por dataframe
    valores_nulos_df = dataframe.isnull().sum().sum()

    return("Valores nulos por columna", valores_nulos_cols,
           "valores nulos por dataframe", valores_nulos_df)


###Función_4. Sustituye  los valores atípicos de las columnas numéricas con el método de “Rango intercuartílico” ###

def identificar_valores_atipicos2(dataframe):
    import pandas as pd
    cuantitativas2 = dataframe.select_dtypes(include=["float64","int64","float","int"])
    cualitativas2 = dataframe.select_dtypes(include=["object","datetime","category"])
    y=cuantitativas2
    percentile25=y.quantile(0.25)
    percintile75=y.quantile(0.75)
    iqr = percintile75-percentile25
    limite_superior_iqr = percintile75 + 1.5*iqr
    limite_inferior_iqr = percentile25 - 1.5*iqr
    atipicos = cuantitativas2[(y<=limite_superior_iqr)&(y>=limite_inferior_iqr)]
    print(atipicos.isnull().sum())
    df_a_limpiar = atipicos.copy()
    df_a_limpiar = df_a_limpiar.fillna(round(atipicos.mean(),1))
    Datos_limpios = pd.concat([cualitativas2, df_a_limpiar], axis=1)
    return Datos_limpios