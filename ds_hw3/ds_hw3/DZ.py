import requests
from bs4 import BeautifulSoup
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


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

# Функція для з'єднання з базою данних
def Connect_to_db_mongo(
    uri="mongodb+srv://olegniedz:Oleg77918082@cluster0.swjmkbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
):
    # Create a new db_connection and connect to the server
    db_connection = MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    try:
        db_connection.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return db_connection
    except Exception as e:
        print(e)
        return None


# Основна логіка
def main():
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

    # Зберегти дані у БД
    uri = "mongodb+srv://olegniedz:Oleg77918082@cluster0.swjmkbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db_connection = Connect_to_db_mongo(uri=uri)

    if db_connection:
        quotes_collection = db_connection.DS03.quotes
        with open("quotes.json", encoding="utf-8") as f:
            quotes = json.load(f)
        quotes_collection.drop()
        quotes_collection.insert_many(quotes)

        authors_collection = db_connection.DS03.authors
        with open("authors.json", encoding="utf-8") as f:
            authors = json.load(f)
        authors_collection.drop()
        authors_collection.insert_many(authors)


if __name__ == "__main__":
    main()
