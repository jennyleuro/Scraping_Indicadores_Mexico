import locale
from numpy import NaN
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys

#Configuración para decimales con coma y
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Opciones de navegación

options = webdriver.ChromeOptions()
options .add_argument('--start-maximized')
options .add_argument('--disable-extensions')

driver_path =  "D:\Chrome driver\chromedriver.exe"

# Inicializamos el diver, que nos va a controlar la página web
driver = webdriver.Chrome(driver_path, options = options) 

# Inicializar el navegador
driver.get('https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CE183&locale=es')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'button#graph_nodo_2_SE45273')))\
        .click()

driver.switch_to.frame(driver.find_element(By.ID, 'iframeGrafica'))

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'button#btnDatos')))\
        .click()

portafolio= driver.find_elements_by_xpath("//table[@id = 'tableData']//tr[@data-ts]")

portafolio_fecha_text, portafolio_datos_text= [], []

for dato in portafolio:
    portafolio_inv = dato.text.split()

    if(portafolio_inv[0] == '01/10/1999'):
        break
    elif (portafolio_inv[1] == 'N/E'):
        portafolio_datos_text.append(NaN)
        portafolio_fecha_text.append(portafolio_inv[0])
    else:
        dato_text = locale.atof(portafolio_inv[1])
        portafolio_datos_text.append(dato_text)
        portafolio_fecha_text.append(portafolio_inv[0])

#Diccionario con la información
data = {'Periodo': portafolio_fecha_text,
        'Dato': portafolio_datos_text}

df = pd.DataFrame(data, columns=['Periodo', 'Dato'])
df.to_csv('data_portafolio.csv')
print('Se guardó el archivo')

