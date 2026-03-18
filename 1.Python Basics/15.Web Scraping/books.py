import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

books = soup.find_all("h3")

for book in books:
    print(book.text)