#!/usr/bin/env python3
from crawler.crawler import WebCrawler

def main():
    # Example usage of the WebCrawler
    crawler = WebCrawler(delay=2)  # Be polite with a 2-second delay between requests
    
    # Start URL to crawl
    start_url = "https://example.com"
    
    # Crawl the website (limited to 5 pages for this example)
    results = crawler.crawl(start_url, max_pages=5)
    
    # Print the results
    print(f"Crawled {len(results)} pages:")
    for url in results:
        print(f" - {url}")

if __name__ == "__main__":
    main()