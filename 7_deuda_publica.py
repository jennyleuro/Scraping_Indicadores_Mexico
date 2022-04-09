from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

# Inicializar el navegador
driver.get('https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CG7&sector=9&locale=es')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input#exportarSeriesFormatoXLS')))\
        .click()

nombre_archivo = fmex.getDownLoadedFileName(180, driver) #Se esperan 3 minutos a que se descargue

#Leyendo el archivo
archivo_excel = pd.ExcelFile(nombre_archivo)
df = archivo_excel.parse('Hoja1', skiprows=17)

#Filtrando sólo la información necesaria
filtro = df['Fecha']>datetime.strptime("1999/12/31", "%Y/%m/%d")
df = df[filtro]

#Saldos a Final del Periodo
df = df[['Fecha','SG193', 'SG199']] #SG193 = Económica Amplia, SG199 = Consolidada con Banco de México

#Definiendo Fecha como index
df = df.set_index('Fecha')

#Calculo de la deuda total
df_deuda_total = pd.DataFrame()
df_deuda_total['Deuda Pública']= df['SG193'] + df['SG199']

df_deuda_total.to_csv('data_deuda.csv')
print('Se guardó el archivo')
