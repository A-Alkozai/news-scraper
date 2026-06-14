# News Scraper

A Python-based news aggregation system that extracts articles from RSS feeds, filters and processes content, and stores structured data in a PostgreSQL database using Docker. The project was initially developed as a stepping stone toward building a full API-based news service.

Development was later paused due to university workload and considerations around data sourcing and compliance with content usage policies.

---

## Overview

This project collects RSS feeds from a predefined list, extracts article metadata, filters non-article content, and stores clean entries into a structured database. It was designed with scalability in mind, with the original goal of evolving into a full REST API service.

---

## Features

- RSS feed parsing and extraction  
- Article filtering to remove non-relevant or malformed entries  
- Rate limiting to reduce request load on sources  
- Rotating user-agent system for improved reliability  
- Structured storage of articles in PostgreSQL  
- Dockerised database environment for easy setup  
- Deduplication and schema-based storage design  

---

## Technologies Used

- Python  
- PostgreSQL  
- Docker / Docker Compose  
- RSS (XML parsing)  
- Requests / HTTP libraries  

---

## Architecture

The system follows a modular pipeline:

1. **Feed Reader** – Reads RSS feed URLs from a configuration file  
2. **Scraper Engine** – Extracts article metadata from feeds  
3. **Filter Layer** – Removes non-article or irrelevant entries  
4. **Rate Limiter** – Controls request frequency per source  
5. **Storage Layer** – Inserts structured data into PostgreSQL  
6. **Docker Environment** – Runs database in isolated container  

The database schema includes article title, source, publication date, and content URL.

---

## My Contribution

This was a solo project. I designed and implemented the full system, including:

- RSS feed ingestion system  
- Article scraping and parsing logic  
- Database schema design and integration  
- Docker setup for PostgreSQL  
- Rate limiting and user-agent rotation system  
- Data filtering and deduplication logic  

---

## Future Improvements

Although development is currently paused, the intended next steps were:

- Convert scraper into a REST API service (FastAPI or Flask)  
- Add authentication layer for API usage  
- Implement asynchronous scraping for scalability  
- Add web dashboard for viewing articles  
- Introduce topic classification / tagging system  
- Deploy system using cloud infrastructure  

---

## Repository Structure

```text
main.py                  # Entry point
scraper/                 # RSS parsing and scraping logic
database/                # DB connection + schema setup
services/               # Rate limiting, request handling
docker-compose.yml      # PostgreSQL container setup
rss-links.txt           # Source feed list
