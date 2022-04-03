from datetime import datetime
import pandas as pd

path = "data_tipo_cambio_mex.csv"

df = pd.read_csv(path)

print('DATAFRAME EN BRUTO')
print(df.head())

df['Fecha'] = pd.to_datetime(df['Fecha'])

print('DF CON FECHA CAMBIADA')
print(df.head)

df = df.set_index('Fecha')

print('DF CON FECHA COMO INDEX')
print(df.head)

df.dropna()
 
mensual = df.resample('M').mean()

#print(df.tail)
#print(mensual.tail)




 



    
