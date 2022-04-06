import locale
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from numpy import NaN

#Configuración para decimales con coma y
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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

driver.switch_to.frame(driver.find_element(By.ID, 'iframeGrafica'))

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'button#btnDatos')))\
        .click()

reservas= driver.find_elements_by_xpath("//table[@id = 'tableData']//tr[@data-ts]")

reservas_fecha_text, reservas_datos_text= [], []

for dato in reservas:
    reserva_int = dato.text.split()

    if(reserva_int[0] == '31/12/1999'):
        break
    elif (reserva_int[1] == 'N/E'):
        reservas_datos_text.append(NaN)
        reservas_fecha_text.append(reserva_int[0])
    else:
        dato_text = locale.atof(reserva_int[1])
        reservas_datos_text.append(dato_text)
        reservas_fecha_text.append(reserva_int[0])
      
#Diccionario con la información
data = {'Periodo': reservas_fecha_text,
        'Dato': reservas_datos_text}

df = pd.DataFrame(data, columns=['Periodo', 'Dato'])

#Cambio de formato para fecha
df['Periodo'] = pd.to_datetime(df['Periodo'], format='%d/%m/%Y')

#Fecha como index
df = df.set_index('Periodo')

#Eliminando valores nulos para no afectar el promedio
df.dropna() 

#Promedio mensual
prom_mensual = df.resample('M').mean()

prom_mensual.to_csv('data_reservas_int.csv')
print('Se guardó el archivo')

