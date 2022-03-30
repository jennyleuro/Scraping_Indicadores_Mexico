from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from lxml import html
import requests

# Opciones de navegación

options = webdriver.ChromeOptions()
options .add_argument('--start-maximized')
options .add_argument('--disable-extensions')

driver_path =  "D:\Chrome driver\chromedriver.exe"

driver = webdriver.Chrome(driver_path, options = options)

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
        .send_keys('01/01/2005')     

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input.botonesSIE')))\
        .click()

driver.switch_to.window(driver.window_handles[1])

encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

tipo_cambio_fecha = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='left']/td")
tipo_cambio_datos = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='right']/td")

del tipo_cambio_datos[len(tipo_cambio_fecha):]

fecha_text_list, datos_text_list = [], []

for dato in tipo_cambio_datos:
    valor_text = dato.text
    datos_text_list.append(valor_text)

for fecha in tipo_cambio_fecha:
    fecha_text = fecha.text
    fecha_text_list.append(fecha_text)

diccionario_tipo_cambio = {'Fecha': fecha_text_list,
             'Tipo de Cambio': datos_text_list
            }

df = pd.DataFrame(diccionario_tipo_cambio, columns=['Fecha', 'Tipo de Cambio'])
df.to_csv('data_tipo_cambio_mex.csv')
print("Se extrajo la información y se guardó en csv")


