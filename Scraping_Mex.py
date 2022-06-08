from calendar import month
import funciones_mex as fmex
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

# Extrayendo indicadores méxico
try:
  df_reservas = fmex.reservasMex(driver)
  df_tipo_cambio = fmex.tipoDeCambio(driver)
  df_exportaciones = fmex.exportaciones(driver)
  df_liquidez_solvencia = fmex.liquidezSolvencia(driver)
  df_portafolio = fmex.inversionPortafolio(driver)
  df_deuda = fmex.deudaPublica(driver)
  df_PIB = fmex.PIB(driver)
except:
  print('Error al extraer los datos')

indicadores_mensuales = [df_reservas, df_tipo_cambio, df_exportaciones, df_liquidez_solvencia, df_deuda]

writer = pd.ExcelWriter('indicadores_trimestrales.xlsx')

for indicador in indicadores_mensuales:
  quarterly = indicador.resample('Q').mean()
  quarterly = quarterly.reset_index()
  lista_fechas = []
  for fecha in quarterly['Fecha']:
    dias = int(fecha.strftime('%d'))-1
    fecha_nueva = fecha - datetime.timedelta(days = dias)
    lista_fechas.append(fecha_nueva)
  quarterly['Fecha'] = lista_fechas
  quarterly = quarterly.set_index('Fecha')
  columns_names = list(quarterly.columns.values)
  quarterly.to_excel(writer, sheet_name = columns_names[0])


lista_fechas_PIB = []
for fecha in df_PIB['Fecha']:
  fecha_nueva_PIB = datetime.datetime.strptime(fecha, '%Y/%m')
  lista_fechas_PIB.append(fecha_nueva_PIB)
df_PIB['Fecha'] = lista_fechas_PIB
df_PIB = df_PIB.set_index('Fecha')
df_PIB = df_PIB.sort_index()
df_PIB.to_excel(writer, 'PIB')

df_portafolio = df_portafolio.reset_index()
lista_fechas_portafolio = []
for fecha in df_portafolio['Fecha']:
  fecha_nueva_portafolio = fecha - relativedelta(months = 1)
  lista_fechas_portafolio.append(fecha_nueva_portafolio)
df_portafolio['Fecha'] = lista_fechas_portafolio
df_portafolio = df_portafolio.set_index('Fecha')
df_PIB = df_PIB.sort_index()
df_portafolio.to_excel(writer, 'Inversión de Portafolio')

writer.save()

print('Se extrajo y guardó la información')

