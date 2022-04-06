from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time 

# Opciones de navegación
options = webdriver.ChromeOptions()
options .add_argument('--start-maximized')
options .add_argument('--disable-extensions')
options.add_experimental_option('prefs', {
    "download.default_directory": "D:\\2022-I\Práctica I\Primera asignación\México"
})

driver_path =  "D:\Chrome driver\chromedriver.exe"
driver = webdriver.Chrome(driver_path, options = options)

# Inicializar el navegador
driver.get('https://www.inegi.org.mx/sistemas/bie/')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a#PT1000')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a#PT10000520')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a#PT100005200070')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a#PT1000052000700070')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'a#PT10000520007000700005')))\
        .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//a[@id = "127598"]/i')))\
        .click()

time.sleep(5)

exportaciones = driver.find_elements_by_xpath("//div[@id = 'ctl00_cphPage_ContentUpdatePanel2']/center//tr[@valign='top']")

periodos, datos = [], []

for exportacion in exportaciones:
    export = exportacion.text.split()

    if(export[0] == '1999/12'):
        break
    else:
        periodos.append(export[0])
        datos.append(export[1])

#Diccionario con la información
data = {'Periodo': periodos,
        'Dato': datos}

df = pd.DataFrame(data, columns=['Periodo', 'Dato'])
df.to_csv('data_exportaciones.csv')
print('Se guardó el archivo')