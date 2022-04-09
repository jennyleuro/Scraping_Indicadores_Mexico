import locale
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from numpy import NaN
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def browserOptions(driverpath):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('prefs', {
    "download.default_directory": "D:\\2022-I\Práctica I\Primera asignación\México"
    })
    driver_path = driverpath
    driver = webdriver.Chrome(driver_path, options = options) 
    return driver

def infoSplitDf(list_info, indicador):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    fecha_text, datos_text= [], []
    
    for dato in list_info:
        info_text = dato.text.split()
        if(info_text[0] == '31/12/1999' or info_text[0] == '1999/04' or info_text[0] == '1999/12'):
            break
        elif (info_text[1] == 'N/E'):
            datos_text.append(NaN)
            fecha_text.append(info_text[0])
        else:
            dato_text = locale.atof(info_text[1])
            datos_text.append(dato_text)
            fecha_text.append(info_text[0])

    data = {'Fecha': fecha_text,
        indicador: datos_text}
    df = pd.DataFrame(data, columns=['Fecha', indicador])

    return df

def dataCleaning(df, date_format):
    df['Fecha'] = pd.to_datetime(df['Fecha'], format= date_format)
    df = df.set_index('Fecha')
    df.dropna() 
    df = df.sort_index()
    return df

def getDownLoadedFileName(waitTime, driver):
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

def reservasMex(driver):
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
    
    #Limpieza de datos y almacenamiento en Data Frame
    reservas= driver.find_elements_by_xpath("//table[@id = 'tableData']//tr[@data-ts]")
    df = infoSplitDf(reservas, 'Reservas')    
    df = dataCleaning(df, '%d/%m/%Y')
    prom_mensual = df.resample('M').mean()

    return prom_mensual

def tipoDeCambio(driver):
    # Inicializar el navegador
    driver.get('https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=sp')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'a.liga')))\
            .click()

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'input.renglonNon')))\
            .send_keys(Keys.CONTROL, 'a')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'input.renglonNon')))\
            .send_keys(Keys.BACKSPACE)

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'input.renglonNon')))\
            .send_keys('01/01/2000')     

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'input.botonesSIE')))\
            .click()

    driver.switch_to.window(driver.window_handles[1])

    tipo_cambio_fecha = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='left']/td")
    tipo_cambio_datos = driver.find_elements_by_xpath("//body//table//td[@valign='top' and @align='center']//tr[@align='right']/td")

    del tipo_cambio_datos[len(tipo_cambio_fecha):]

    fecha_text_list, datos_text_list = [], []

    for dato in tipo_cambio_datos:
        dato_text = dato.text

        if(dato_text == 'N/E'):
            datos_text_list.append(NaN)
        else:
            datos_text_list.append(float(dato_text))

    for fecha in tipo_cambio_fecha:
        fecha_text = fecha.text
        fecha_text_list.append(fecha_text)

    diccionario_tipo_cambio = {'Fecha': fecha_text_list,
                'Tipo de Cambio': datos_text_list
                }

    df = pd.DataFrame(diccionario_tipo_cambio, columns=['Fecha', 'Tipo de Cambio'])

    #Limpieza de datos
    df = dataCleaning(df, '%d/%m/%Y')

    #Promedio mensual
    prom_mensual = df.resample('M').mean()
    return prom_mensual

def exportaciones(driver):
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
    df = infoSplitDf(exportaciones, 'Exportaciones')

    #Limpieza de datos
    df = dataCleaning(df, '%Y/%m')
    return df

def liquidezSolvencia(driver):
    driver.get('https://www.cnbv.gob.mx/SECTORES-SUPERVISADOS/BANCA-MULTIPLE/Paginas/Información-Estadística.aspx')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, 
        '//p[@style = "text-align:left;"]/a')))\
            .click()

    driver.switch_to.window(driver.window_handles[-1])

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, 
        '//table[@class="MsoNormalTable "]/tbody/tr/td/div/span/a/span[@lang="ES" and @style="font-size: 10pt; text-decoration: none; color: blue"]')))\
            .click()

    driver.switch_to.window(driver.window_handles[-1])

    excel_url = driver.find_element(By.XPATH, '//tr[@id="1"]//a').get_attribute('href')

    archivo_excel = pd.ExcelFile(excel_url)

    df = archivo_excel.parse('Hoja2', skiprows=2)

    #Cambiando el indice del data frame
    df = df.set_index('Indicadores del Balance General (millones de pesos corrientes)')

    #Eliminando columnas innecesarias
    df = df.drop(['Unnamed: 0'], axis = 1)

    #Cambiando Columnas por filas
    df = df.transpose()

    #Data frame con sólo la info necesaria
    df_resumen = df[['Pasivo', 'Activo','Capital contable']]

    #Data frame liquidez y solvencia calculada
    df_liquidez_solvencia = pd.DataFrame()
    df_liquidez_solvencia['Liquidez'] = df_resumen['Pasivo']/df_resumen['Activo']
    df_liquidez_solvencia['Solvencia'] = df_resumen['Capital contable']/df_resumen['Activo']
    df_liquidez_solvencia = df_liquidez_solvencia.sort_index()

    return df_liquidez_solvencia

def inversionPortafolio(driver):
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

    #Limpieza de datos
    df = infoSplitDf(portafolio, 'Inversión de Portafolio')    
    df = dataCleaning(df, '%d/%m/%Y')

    return df

def deudaPublica(driver):
    # Inicializar el navegador
    driver.get('https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CG7&sector=9&locale=es')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'input#exportarSeriesFormatoXLS')))\
            .click()

    nombre_archivo = getDownLoadedFileName(180, driver) #Se esperan 3 minutos a que se descargue

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
    df_deuda_total = pd.DataFrame()
    df_deuda_total['Deuda Pública'] = df['SG193'] + df['SG199']
    df_deuda_total = df_deuda_total.sort_index()

    return df_deuda_total

def PIB(driver):
    # Inicializar el navegador
    driver.get('https://www.inegi.org.mx/sistemas/bie/?idserPadre=1000025501150150')

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.XPATH, 
        '//a[@id = "493717"]/i')))\
            .click()
    
    time.sleep(5)

    pib = driver.find_elements_by_xpath("//div[@id = 'ctl00_cphPage_ContentUpdatePanel2']/center//tr[@valign='top']")

    #Separando la info, pasando los datos a números y obteniendo data frame
    df = infoSplitDf(pib, 'PIB')    

    #Limpieza de datos
    
    return df

def tasaCrecimiento(df, columna):
    tasa_crecimiento_list = [NaN]
    for i in range(1, len(df[columna]-1)):
        v2 = df.iloc[i][columna]
        v1 = df.iloc[i-1][columna]
        tasa_crecimiento = ((v2-v1)/v1)*100
        tasa_crecimiento_list.append(tasa_crecimiento)
    df['Tasa Crecimiento'] = tasa_crecimiento_list    
    return df

