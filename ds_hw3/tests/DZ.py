import requests
from bs4 import BeautifulSoup
import json


# Функція для отримання вмісту сторінки
def get_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# Функція для отримання цитат та авторів
def get_quotes_and_authors(soup:BeautifulSoup):
    quotes = []
    authors = []

    for quote in soup.find_all("div", class_="quote"):
        quote_tags = (
            quote.find("div", class_="tags").get_text().strip().split("\n")[2::]
        )
        quote_author = quote.find("small", class_="author").get_text()
        quote_text = quote.find("span", class_="text").get_text()
        author_href = quote.find("a").get("href")
        quotes.append(
            {
                "tags": quote_tags,
                "author": quote_author,
                "quote": quote_text,
            }
        )
        authors.append({"fullname": author_href})

    return quotes, authors


# Функція для отримання інформації про авторів з окремої сторінки
def get_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    fullname = soup.find("h3", class_="author-title").get_text()
    born_date = soup.find("span", class_="author-born-date").get_text()
    born_location = soup.find("span", class_="author-born-location").get_text()
    description = soup.find("div", class_="author-description").get_text().strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }


# Основна логіка
quotes = []
authors = []

for page_number in range(1, 11):  # 10 сторінок
    url = f"http://quotes.toscrape.com/page/{page_number}/"
    soup = get_page_content(url)
    page_quotes, page_authors = get_quotes_and_authors(soup)
    quotes.extend(page_quotes)
    authors.extend(page_authors)

    for author in page_authors:
        author_url = f'http://quotes.toscrape.com{author["fullname"]}/'
        author_info = get_author_info(author_url)
        author.update(author_info)


# Зберегти результати у JSON-файли
with open("quotes.json", "w",encoding='utf-8') as f:
    json.dump(quotes, f,ensure_ascii=False,indent=4)

with open("authors.json", "w",encoding='utf-8') as f:
    json.dump(authors, f,ensure_ascii=False,indent=4)
