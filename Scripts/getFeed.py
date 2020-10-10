import os

from getLocation import getAdress
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
option.headless = True

browser = webdriver.Chrome(
    executable_path=r"D:\Documentos\GitProjects\tcc_TransporteUrbano\chromedriver\chromedriver.exe", options=option
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

enderecos = []
for x in datas:
    enderecos.append(getAdress(x))

ret = []
x = 0
for i in evento:
    obj = {}
    obj["nome"] = evento[x]
    obj["link"] = links[x]
    obj["data"] = datas[x]
    obj["endereco"] = enderecos[x][0]
    obj["latitude"] = enderecos[x][1]
    obj["longitude"] = enderecos[x][2]
    ret.append(obj)
    x += 1

print(ret)
