
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd 

#Método para obtener el nombre del archivo descargado
def getDownLoadedFileName(waitTime):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break

# Opciones de navegación

options = webdriver.ChromeOptions()
options .add_argument('--start-maximized')
options .add_argument('--disable-extensions')

#Directorio por defecto para las descargas
options.add_experimental_option('prefs', {
    "download.default_directory": "D:\\2022-I\Práctica I\Primera asignación\México"
})

driver_path =  "D:\Chrome driver\chromedriver.exe"

# Inicializamos el diver, que nos va a controlar la página web
driver = webdriver.Chrome(driver_path, options = options) 

# Inicializar el navegador
driver.get('https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CG7&sector=9&locale=es')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
    'input#exportarSeriesFormatoXLS')))\
        .click()

nombre_archivo = getDownLoadedFileName(180) #Se esperan 3 minutos a que se descargue

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
df_deuda_total = df['SG193'] + df['SG199']

df_deuda_total.to_csv('data_deuda.csv')
print('Se guardó el archivo')