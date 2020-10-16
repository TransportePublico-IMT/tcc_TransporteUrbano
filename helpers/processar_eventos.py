import os
from os.path import dirname, join
import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import geopy.distance
import googlemaps
import pandas as pd
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3

# Create .env file path.
dotenv_path = join(dirname(__file__), "../.ENV")
load_dotenv(dotenv_path)
API = os.getenv("GOOGLE_MAPS")

geolocator = GoogleV3(api_key=API)

def get_adress(nome):
    name = nome
    try:
        location = geolocator.geocode(name)
        endereco = [location.address, location.latitude, location.longitude]
    except Exception as e:
        endereco = [None, None, None]
    return endereco

def get_date(string):
    dict_meses = {
        "janeiro": "01",
        "fevereiro": "02",
        "março": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12"
    }
    data = []
    word_list = string.replace("/", " ").split(" ")
    for i in word_list:
        if i.isdigit():
            data.append(i) #dia
        if i in dict_meses:
            data.append(dict_meses[i]) #mes
    try:
        ultimo_elemento = len(data[-1:][0])
    except:
        ultimo_elemento = 5
    if len(data) == 2 or ultimo_elemento < 4:
        now = datetime.datetime.now()
        data.append(str(now.year)) #ano
    if len(data) > 3:
        data = data[-3:]
    if len(data) == 3:
        data_str = '-'.join(list(reversed(data)))
        return data_str
    else:
        return None

def get_eventos():
    option = webdriver.ChromeOptions()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless')
    option.add_argument(" — incognito")
    option.add_argument('log-level=3')
    option.add_experimental_option('excludeSwitches', ['enable-logging'])

    if os.getenv("AMBIENTE").lower() == 'des':
        chromedriver_path = os.getcwd() + "\\chromedriver\\chromedriver.exe"
    elif os.getenv("AMBIENTE").lower() == 'prod':
        chromedriver_path = os.getcwd() + "/chromedriver/chromedriver"

    browser = webdriver.Chrome(
        executable_path=chromedriver_path,
        options=option
    )
    browser.get(
        "https://premier.ticketsforfun.com.br/search/searchresults.aspx?k=s%C3%A3o+paulo"
    )
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@class='logo-footer']"))
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    nome_elements = browser.find_elements_by_xpath("//h3[@class='nome-evento']")
    evento = [x.text for x in nome_elements]

    links = []
    for nome in evento:
        link_elemento = browser.find_element_by_link_text(nome)
        links.append(link_elemento.get_attribute("href"))

    datas = []
    for link in links:
        browser.get(link)
        try:
            WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((By.XPATH, "//img[@class='logo-footer']"))
            )
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
        data = ""
        data_elements = browser.find_elements_by_xpath("//span[@class='sr-only']")
        for x in data_elements:
            if "São Paulo" in x.text:
                data = x.text
            elif "Săo Paulo" in x.text:
                data = x.text
        datas.append(data)

    browser.close()
    browser.quit()

    enderecos = []
    for x in datas:
        enderecos.append(get_adress(x))

    ret = []
    x = 0
    for i in evento:
        obj = {}
        obj["nome"] = evento[x]
        obj["link"] = links[x]
        obj["data_info"] = datas[x]
        obj["data"] = get_date(datas[x])
        obj["endereco"] = enderecos[x][0]
        obj["latitude"] = enderecos[x][1]
        obj["longitude"] = enderecos[x][2]
        ret.append(obj)
        x += 1

    return ret
