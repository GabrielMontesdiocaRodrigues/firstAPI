import requests
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from main import addBook
from dataBase import SessionLocal

# Configura WebDriver
service = Service()
option = webdriver.ChromeOptions()

# Cria instância webdriver
driver = webdriver.Chrome(option, service, False)

# Site para scrape
url = 'https://books.toscrape.com/'
driver.get(url)


def returnPrice(price: str):
    return float(price.replace('£', ''))


def getCotation():
    cotation_json = requests.get(
        "https://economia.awesomeapi.com.br/last/EUR-BRL").json()
    return float(cotation_json['EURBRL']['bid'])


def getBottonNext():
    try:
        return driver.find_element(By.CLASS_NAME, 'next').find_element(By.TAG_NAME, 'a')
    except exceptions.NoSuchElementException:
        return None


def addBooks(new_books: list, old_books: list):
    for new_book in new_books:
        old_books.append(new_book)
    return old_books


def getBooks():
    books_title = []
    books_price = []
    botton_next = getBottonNext()
    cotacao = getCotation()
    i = 0
    while botton_next != None:

        title_web_elements = driver.find_elements(By.TAG_NAME, 'a')
        price_web_elements = driver.find_elements(By.CLASS_NAME, 'price_color')
        books_title_pg = [
            title_web_element.get_attribute("title")
            for title_web_element in title_web_elements
            if title_web_element.get_attribute("title") != ''
        ]
        book_price_pg = [
            price_web_element.text
            for price_web_element in price_web_elements
        ]
        books_title = addBooks(books_title_pg, books_title)
        books_price = addBooks(book_price_pg, books_price)

        for title, price in zip(books_title, books_price):
            addBook('post', book_title=title,
                    book_price=round(returnPrice(price) * cotacao, 2), db=SessionLocal())
        botton_next.click()
        botton_next = getBottonNext()


getBooks()
