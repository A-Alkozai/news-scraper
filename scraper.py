from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import requests
import psycopg
import os

# Header to disguise connection as a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Returns a connection to the database
def getConnection():
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

# Returns a list of links from the database which have not been scraped
def getRSSLinks():
    links = []
    connection = getConnection()
    with connection.cursor() as cur:
        cur.execute("""
            SELECT link FROM articles 
            WHERE original_content IS NULL;
        """)
        for link in cur:
            links.append(link[0])
    connection.close()
    return links

# Adds content to database
def addContent(content, link):
    content = " ".join(content)
    connection = getConnection()
    with connection.cursor() as cur:
        cur.execute("""
            UPDATE articles 
            SET original_content = %s
            WHERE link = %s""",
            (content, link),
        )
    connection.commit()
    connection.close()

# Scrapes given link
def scrapeLink(link):
    response = requests.get(link, headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    if soup.article != None:
        main = soup.find_all("article")
        content = []
        for data in main:
            content = content + [p.get_text(strip=True) for p in data.find_all("p")]
        addContent(content, link)

links = getRSSLinks()
for link in links:
    scrapeLink(link)