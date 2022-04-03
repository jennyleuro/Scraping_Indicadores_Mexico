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
driver.get('https://www.inegi.org.mx/sistemas/bie/?idserPadre=1000025501150150')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//a[@id = "493717"]/i')))\
        .click()
 
time.sleep(5)

PIB = driver.find_elements_by_xpath("//div[@id = 'ctl00_cphPage_ContentUpdatePanel2']/center//tr[@valign='top']")

periodos, datos = [], []

for dato in PIB:
    PIB_trimestral = dato.text.split()

    if(PIB_trimestral[0] == '2004/04'):
        break
    else:
        periodos.append(PIB_trimestral[0])
        datos.append(PIB_trimestral[1])

#Diccionario con la información
data = {'Periodo': periodos,
        'Dato': datos}

df = pd.DataFrame(data, columns=['Periodo', 'Dato'])
df.to_csv('data_PIB.csv')
print('Se guardó el archivo')