import feedparser
import requests


# Parses the RSS Feed XML
def parseRSS(url):
    response = requests.get(url) # Fetch content manually - MacOS may silently fail with feedparser 
    feed = feedparser.parse(response.content) # Parse the content
    return feed

# Reads each news entry in the RSS Feed
def getEntries(feed):
    for entry in feed:
        print(entry.title)
        print(entry.description)
        print(entry.link)
        print(entry.guid)
        print(entry.published)
        if "media_thumbnail" in entry:
            print(entry.media_thumbnail)
        elif "media_content" in entry:
            print(entry.media_content)
        print("\n\n")


# Reads the rss-links.txt
with open("rss-links.txt") as list:
    for rss in list:
        rss = rss.strip() # Remove whitespaces and \n 
        if rss.startswith("http"): # Ignore non links
            rss = parseRSS(rss)
            getEntries(rss.entries)