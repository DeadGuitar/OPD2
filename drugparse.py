from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse(link):
    titles = []
    prices = []
    dlinks = []
    photos = []
    proxies = {
        'http': 'http://proxy.omgtu:8080',
        'https': 'http://proxy.omgtu:8080'
    }
    url = 'https://apteka.ru/omsk/search/?q='+ link

    driver = webdriver.Edge()
    # load the web page
    driver.get(url)

    # set maximum time to load the web page in seconds
    driver.implicitly_wait(6)

    table = driver.find_element(By.CLASS_NAME, "CardsGrid")
    cards = table.find_elements(By.CLASS_NAME, "catalog-card__name.emphasis")
    roubletags = table.find_elements(By.CLASS_NAME, "moneyprice__roubles")
    urls = table.find_elements(By.CLASS_NAME, "catalog-card__link")
    pics = table.find_elements(By.CLASS_NAME, "catalog-card__photos")

    for drug in cards:
        drugname = drug.get_attribute("title")
        titles.append(drugname)

    for roubles in roubletags:
        prices.append(roubles.text)

    for lin in urls:
        dlin = lin.get_attribute("href")
        dlinks.append(dlin)

    for pic in pics:
        photo = pic.get_attribute("href")
        photos.append(photo)
    if titles != []:
        out = [titles, prices, dlinks, photos]
    else:
        out = 0
    return out
