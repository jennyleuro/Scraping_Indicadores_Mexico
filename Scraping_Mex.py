import funciones_mex as fmex
import pandas as pd
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

#Extrayendo indicadores méxico
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
indicatores_trimestrales = []

writer = pd.ExcelWriter('indicadores_trimestrales.xlsx')

for indicador in indicadores_mensuales:
    quarterly = indicador.resample('Q').mean()
    columns_names = list(quarterly.columns.values)
    quarterly.to_excel(writer, sheet_name = columns_names[0])


df_PIB.to_excel(writer, sheet_name= 'PIB')
df_portafolio.to_excel(writer, sheet_name= 'Inversión de Portafolio')

writer.save()
writer.close()

