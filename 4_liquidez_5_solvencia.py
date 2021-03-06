from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

# Inicializar el navegador
driver.get('https://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/BANCA-MULTIPLE/Paginas/Información-Estadística.aspx')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//p[@style = "text-align:left;"]/a')))\
        .click()

driver.switch_to.window(driver.window_handles[1])

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//table[@class="MsoNormalTable "]/tbody/tr/td/div/span/a/span[@lang="ES" and @style="font-size: 10pt; text-decoration: none; color: blue"]')))\
        .click()

driver.switch_to.window(driver.window_handles[2])

excel_url = driver.find_element(By.XPATH, '//tr[@id="1"]//a').get_attribute('href')

archivo_excel = pd.ExcelFile(excel_url)

df = archivo_excel.parse('Hoja2', skiprows=2)

#Cambiando el indice del data frame
df = df.set_index('Indicadores del Balance General (millones de pesos corrientes)')

#Eliminando columnas innecesarias
df = df.drop(['Unnamed: 0'], axis = 1)

#Cambiando Columnas por filas
df = df.transpose()


#Data frame con sólo la info necesaria
df_resumen = df[['Pasivo', 'Activo','Capital contable']]

#Data frame liquidez calculada
df_liquidez = pd.DataFrame()
df_liquidez['Liquidez'] = df_resumen['Pasivo']/df_resumen['Activo']

#Data frame solvencia calculada
df_solvencia = pd.DataFrame()
df_solvencia['Solvencia'] = df_resumen['Capital contable']/df_resumen['Activo']

df_solvencia.to_csv('data_solvencia.csv')
df_liquidez.to_csv('data_liquidez.csv')

print('Se guardaron los archivos')


