import pandas as pd
import funciones_mex as fmex

excel_doc = 'indicadores_trimestrales.xlsx'
archivo_excel = pd.ExcelFile(excel_doc)

try:
    df_reservas = archivo_excel.parse('Reservas')
    df_tipo_cambio = archivo_excel.parse('Tipo de Cambio')
    df_exportaciones = archivo_excel.parse('Exportaciones')
    df_liquidez_solvencia = archivo_excel.parse('Liquidez')
    df_portafolio = archivo_excel.parse('Inversión de Portafolio')
    df_deuda = archivo_excel.parse('Deuda Pública')
    df_PIB = archivo_excel.parse('PIB')
except:
    print('Error al cargar los datos')

indicadores_dolares = [df_reservas, df_PIB, df_portafolio]

#Calculo de tasas de crecimiento
for indicador in indicadores_dolares:
    columns_names = list(indicador.columns.values)
    indicador = fmex.tasaCrecimiento(indicador, columns_names[-1])

#Deuda pública/ Exportaciones
df_deuda_export = df_deuda['Deuda Pública']/df_exportaciones['Exportaciones']

indicadores_listos = [df_deuda_export, df_liquidez_solvencia, df_PIB, df_portafolio, df_reservas, df_tipo_cambio]
 


