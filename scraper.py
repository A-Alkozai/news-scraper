from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import requests
import psycopg
import random
import time
import os

# Max number of articles you will scrape per minute
MAX_SCRAPE_PER_MINUTE = 25

# User agents to disguise connection as a browser
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36 Edg/116.0.1938.81",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

# Returns a random user agent
def getHeader():
    return {"User-Agent": random.choice(USER_AGENTS)}

# Random delay to prevent throttling request rate
def getDelay():
    avg = 60 / MAX_SCRAPE_PER_MINUTE
    time.sleep(random.uniform(avg-2, avg+2))

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
    response = requests.get(link, getHeader(), timeout=(3, 10))
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
    getDelay()