from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

class Indicador(Item):
    period = Field()
    #value = Field()

class StackOverFlowSpider(Spider):
    name = "MexicoSpider"

    #user-agent en Scrapy, por medio del objeto custom_settings
    custom_settings = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }

    start_urls = ['https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CF106&locale=es']

    #Definicion de la función de parseo
    def parse(self, response):
        sel = Selector(response) #Es el que permite hacer consultas
        table = sel.xpath("//table[@id = 'tableData']/tbody")

        for row  in table:
            reservas_internacionales = ItemLoader(Indicador(), row) #ItemLoader carga mis items
            reservas_internacionales.add_xpath('period', './/tr/td')
            #reservas_internacionales.add_xpath('value', './/')
            yield reservas_internacionales.load_item() #Una especie de return