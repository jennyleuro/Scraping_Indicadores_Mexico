from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Opciones de navegación

options = webdriver.ChromeOptions()
options .add_argument('--start-maximized')
options .add_argument('--disable-extensions')
#options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver_path =  "D:\Chrome driver\chromedriver.exe"

# Inicializamos el diver, que nos va a controlar la página web
driver = webdriver.Chrome(driver_path, options = options) 

# Inicializar el navegador
driver.get('https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF106&locale=es')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'button#graph_nodo_6_SF43707')))\
        .click()

print('PRINT DE DANIELOS: '+str(driver.find_element_by_id('informacionCuadro')))

WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'button#btnDatos')))\
        .click()

print('PRINT DE DANIELOS 2: '+str(driver.find_element_by_id('informacionCuadro')))

    


