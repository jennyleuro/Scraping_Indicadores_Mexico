from numpy import NaN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

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

#Separando la info, pasando los datos a números y obteniendo data frame
df = fmex.infoSplitDf(portafolio, 'Inversión de Portafolio')    

#Limpieza de datos
df = fmex.dataCleaning(df, '%d/%m/%Y')

df.to_csv('data_portafolio.csv')
print('Se guardó el archivo')