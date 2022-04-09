from numpy import NaN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

# Inicializar el navegador
driver.get('https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=sp')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a.liga')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input.renglonNon')))\
        .send_keys(Keys.CONTROL, 'a')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input.renglonNon')))\
        .send_keys(Keys.BACKSPACE)

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input.renglonNon')))\
        .send_keys('01/01/2000')     

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input.botonesSIE')))\
        .click()

driver.switch_to.window(driver.window_handles[1])

tipo_cambio_fecha = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='left']/td")
tipo_cambio_datos = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='right']/td")

del tipo_cambio_datos[len(tipo_cambio_fecha):]

fecha_text_list, datos_text_list = [], []

for dato in tipo_cambio_datos:
    dato_text = dato.text

    if(dato_text == 'N/E'):
        datos_text_list.append(NaN)
    else:
        datos_text_list.append(float(dato_text))

for fecha in tipo_cambio_fecha:
    fecha_text = fecha.text
    fecha_text_list.append(fecha_text)

diccionario_tipo_cambio = {'Fecha': fecha_text_list,
             'Tipo de Cambio': datos_text_list
            }

df = pd.DataFrame(diccionario_tipo_cambio, columns=['Fecha', 'Tipo de Cambio'])

#Limpieza de datos
df = fmex.dataCleaning(df, '%d/%m/%Y')

#Promedio mensual
prom_mensual = df.resample('M').mean()

prom_mensual.to_csv('data_tipo_cambio_mex.csv')
print("Se extrajo la información y se guardó en csv")

