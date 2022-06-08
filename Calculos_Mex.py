import pandas as pd
import funciones_mex as fmex

excel_doc = 'indicadores_trimestrales.xlsx'
archivo_excel = pd.ExcelFile(excel_doc)

try:
    df_reservas = archivo_excel.parse('Reservas', index_col='Fecha')
    df_tipo_cambio = archivo_excel.parse('Tipo de Cambio', index_col='Fecha')
    df_exportaciones = archivo_excel.parse('Exportaciones', index_col='Fecha')
    df_liquidez_solvencia = archivo_excel.parse('Liquidez', index_col='Fecha')
    df_portafolio = archivo_excel.parse('Inversión de Portafolio', index_col='Fecha')
    df_deuda = archivo_excel.parse('Deuda Pública', index_col='Fecha')
    df_PIB = archivo_excel.parse('PIB', index_col='Fecha')
except:
    print('Error al cargar los datos')

indicadores_dolares = [df_reservas, df_PIB, df_portafolio]

#Calculo de tasas de crecimiento
for indicador in indicadores_dolares:
    columns_names = list(indicador.columns.values)
    indicador = fmex.tasaCrecimiento(indicador, columns_names[-1])

#Deuda pública/ Exportaciones
df_deuda_export = pd.DataFrame()
df_deuda_export['Deuda_Export'] = df_deuda['Deuda Pública']/df_exportaciones['Exportaciones']

#Separando dataframes liquidez y solvencia
df_liquidez, df_solvencia = pd.DataFrame(), pd.DataFrame()
df_liquidez['Liquidez'] = df_liquidez_solvencia['Liquidez']
df_solvencia['Solvencia'] = df_liquidez_solvencia['Solvencia']

indicadores_listos = [df_deuda_export, df_liquidez, df_solvencia, df_PIB, df_portafolio, df_reservas, df_tipo_cambio]

writer = pd.ExcelWriter('episodios_indicadores_Mex.xlsx')

for indicador in indicadores_listos:
    columns_names = list(indicador.columns.values)
    indicador = fmex.espisodios(indicador, columns_names)
    indicador = indicador.style.applymap(fmex.text_format)
    indicador.to_excel(writer, sheet_name = columns_names[0])

writer.save()

print('se calcularon y guardaron los episodios de los indicadores')


