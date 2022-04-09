import locale
from numpy import NaN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time 
import funciones_mex as fmex

# Opciones de navegación
driver = fmex.browserOptions("D:\Chrome driver\chromedriver.exe")

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

#Separando la info, pasando los datos a números y obteniendo data frame
df = fmex.infoSplitDf(exportaciones, 'Exportaciones')

#Limpieza de datos
df = fmex.dataCleaning(df, '%Y/%m')

df.to_csv('data_exportaciones.csv')
print('Se guardó el archivo')