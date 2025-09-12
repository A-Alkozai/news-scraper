from dotenv import load_dotenv
load_dotenv()
import tldextract
import feedparser
import requests
import psycopg
import os


# Dictionary of News Sources
NEWS_SOURCES = {
    "bbc": "BBC News",
    "cbn": "CBN News",
    "nbcnews": "NBC News",
    "cnbc": "CNBC News",
    "mirror": "The Mirror"
}

# Get a connection to the database
def getConnection():
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

# Parses the RSS Feed XML
def parseRSS(url):
    response = requests.get(url) # Fetch content manually - MacOS may silently fail with feedparser 
    feed = feedparser.parse(response.content) # Parse the content
    return feed

# Gets image link from RSS Feed
def getMedia(entry):
    if "media_thumbnail" in entry:
        return entry.media_thumbnail[0].get('url')
    elif "media_content" in entry:
        return entry.media_content[0].get('url')
    return None

# Gets News Source from each RSS Feed
def getSource(feed):
    url = feed[0].get("link")
    domain = tldextract.extract(url).domain
    return NEWS_SOURCES.get(domain)

# Reads each news entry in the RSS Feed
def getEntries(feed):
    connection = getConnection()
    with connection.cursor() as cur:
        for entry in feed:
            mediaURL = getMedia(entry)
            source = getSource(feed)
            cur.execute("""
                INSERT INTO articles (source, title, description, link, guid, published, media)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (link) DO UPDATE
                SET media = EXCLUDED.media
                WHERE articles.media IS NULL;""",
                (source, entry.title, entry.description, entry.link, 
                 entry.guid, entry.published, mediaURL)
            )
    connection.commit()
    connection.close()

# Reads the rss-links.txt
with open("rss-links.txt") as list:
    for rss in list:
        rss = rss.strip() # Remove whitespaces and \n 
        if rss.startswith("http"): # Ignore non links
            rss = parseRSS(rss)
            getEntries(rss.entries)