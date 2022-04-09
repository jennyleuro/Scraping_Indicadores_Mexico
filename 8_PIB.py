from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

# Inicializar el navegador
driver.get('https://www.inegi.org.mx/sistemas/bie/?idserPadre=1000025501150150')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//a[@id = "493717"]/i')))\
        .click()
 
time.sleep(5)

pib = driver.find_elements_by_xpath("//div[@id = 'ctl00_cphPage_ContentUpdatePanel2']/center//tr[@valign='top']")

#Separando la info, pasando los datos a números y obteniendo data frame
df = fmex.infoSplitDf(pib, 'PIB')    

#Limpieza de datos


df.to_csv('data_PIB.csv')
print('Se guardó el archivo')
print(df.head())