import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

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
driver.get('https://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/BANCA-MULTIPLE/Paginas/Información-Estadística.aspx')

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//p[@style = "text-align:left;"]/a')))\
        .click()

driver.switch_to.window(driver.window_handles[1])

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//table[@class="MsoNormalTable "]/tbody/tr/td/div/span/a/span[@lang="ES" and @style="font-size: 10pt; text-decoration: none; color: blue"]')))\
        .click()

driver.switch_to.window(driver.window_handles[2])

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//tr[@id="1"]//img')))\
        .click()

time.sleep(3)

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH, 
    '//tr[@id="37"]//img')))\
        .click()

driver.close()

