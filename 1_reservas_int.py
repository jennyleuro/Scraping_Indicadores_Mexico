from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

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

#Separando la info, pasando los datos a números y obteniendo data frame
df = fmex.infoSplitDf(reservas, 'Reservas')    

#Limpieza de datos
df = fmex.dataCleaning(df, '%d/%m/%Y')

#Promedio mensual
prom_mensual = df.resample('M').mean()

prom_mensual.to_csv('data_reservas_int.csv')
print('Se guardó el archivo')