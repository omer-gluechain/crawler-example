#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import os
import argparse
from urllib.parse import urlparse, urljoin

class WebCrawler:
    def __init__(self, delay=1):
        """
        Initialize the web crawler
        
        Args:
            delay (int): Delay between requests in seconds to be polite to servers
        """
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.visited_urls = set()
    
    def get_html(self, url):
        """
        Fetch the HTML content of a URL
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            str: The HTML content of the page
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html):
        """
        Parse HTML content using BeautifulSoup
        
        Args:
            html (str): HTML content to parse
            
        Returns:
            BeautifulSoup: Parsed HTML
        """
        if html:
            return BeautifulSoup(html, 'html.parser')
        return None
    
    def crawl(self, start_url, max_pages=10):
        """
        Start crawling from a given URL
        
        Args:
            start_url (str): URL to start crawling from
            max_pages (int): Maximum number of pages to crawl
            
        Returns:
            dict: Dictionary with URLs as keys and HTML content as values
        """
        results = {}
        queue = [start_url]
        
        while queue and len(self.visited_urls) < max_pages:
            url = queue.pop(0)
            
            # Skip if we've already visited this URL
            if url in self.visited_urls:
                continue
            
            print(f"Crawling: {url}")
            
            # Mark URL as visited
            self.visited_urls.add(url)
            
            # Get HTML content
            html = self.get_html(url)
            if html:
                # Store the result
                results[url] = html
                
                # Wait before the next request
                time.sleep(self.delay)
            
        return results

def main():
    parser = argparse.ArgumentParser(description='Basic Web Crawler')
    parser.add_argument('url', help='URL to start crawling from')
    parser.add_argument('--max-pages', type=int, default=10, help='Maximum number of pages to crawl')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds')
    parser.add_argument('--output-dir', default='./output', help='Directory to save output files')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize crawler
    crawler = WebCrawler(delay=args.delay)
    
    # Start crawling
    results = crawler.crawl(args.url, max_pages=args.max_pages)
    
    # Save the results
    for i, (url, html) in enumerate(results.items()):
        filename = f"{i+1}_{urlparse(url).netloc.replace('.', '_')}.html"
        filepath = os.path.join(args.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Saved: {filepath}")
    
    print(f"Crawling complete. Visited {len(crawler.visited_urls)} pages.")

if __name__ == "__main__":
    main()