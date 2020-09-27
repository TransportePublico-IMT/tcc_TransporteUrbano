import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

print(os.getcwd() + "/chromeDriver/chromedrivermac")

browser = webdriver.Chrome(
    executable_path=os.getcwd() + "/chromeDriver/chromedrivermac", options=option
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

print("Eventos: \n")
print(evento, "\n")
print("Links: \n")
print(links, "\n")
