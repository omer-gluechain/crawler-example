# crawler-example

A simple web crawler example using Python.

## Required Libraries

- **Requests**: For making HTTP requests
  ```bash
  pip install requests
  ```

- **BeautifulSoup4**: For parsing HTML and XML documents
  ```bash
  pip install beautifulsoup4
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/omer-gluechain/crawler-example.git
   cd crawler-example
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using the Command-Line Interface

The crawler can be run directly from the command line:

```bash
python -m crawler.crawler https://example.com --max-pages 10 --delay 1 --output-dir ./output
```

Arguments:
- `url`: The URL to start crawling from (required)
- `--max-pages`: Maximum number of pages to crawl (default: 10)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--output-dir`: Directory to save output files (default: ./output)

### Using the Python API

You can also use the crawler in your own Python scripts:

```python
from crawler.crawler import WebCrawler

# Initialize the crawler
crawler = WebCrawler(delay=1)

# Start crawling
results = crawler.crawl("https://example.com", max_pages=10)

# Process the results
for url, html in results.items():
    print(f"Crawled: {url}")
    # Process the HTML content as needed
```

Check out `example.py` for a simple example of how to use the WebCrawler class.

## Alternative Libraries

- **Scrapy**: A more comprehensive web crawling framework
- **Selenium**: For JavaScript-heavy websites that require browser automation