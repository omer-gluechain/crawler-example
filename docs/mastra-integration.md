# Mastra.ai Agent Integration Design

## 1. Current Architecture Overview

The current crawler implementation is a simple web crawler built in Python with the following components:

### Core Components

- **WebCrawler class** (in `crawler/crawler.py`): The main class that handles the crawling process.
  - Initializes with customizable delay to be polite to servers
  - Manages a collection of visited URLs
  - Includes methods for fetching HTML content (`get_html`), parsing HTML (`parse_html`), and crawling web pages (`crawl`)

### Functionality

- **HTTP Requests**: Uses the `requests` library to fetch web pages
- **HTML Parsing**: Uses `BeautifulSoup4` to parse HTML content
- **Crawler Logic**: Implements a basic breadth-first URL crawling strategy
- **Output Handling**: Saves crawled HTML content to files (in CLI mode) or returns as a dictionary (in API mode)

### Interface Options

- **Command-line Interface**: Accessible via `python -m crawler.crawler [URL] [OPTIONS]`
- **Python API**: Importable as a module with `from crawler.crawler import WebCrawler`

## 2. Mastra.ai Agent Integration Points

Based on the analysis and the requirement to keep the integration simple and focused on content processing, we've identified the following integration points:

### Primary Integration Point: Content Analysis

The WebCrawler will be extended to leverage Mastra.ai agents for analyzing the content of crawled web pages. The integration will focus on the following capabilities:

1. **Content Extraction**: Using Mastra.ai agents to extract structured data from raw HTML
2. **Content Classification**: Categorizing web page content using AI-powered analysis
3. **Content Summarization**: Generating concise summaries of crawled web pages

### Integration Architecture

We will add a new module called `mastra_agent.py` to the `crawler` package that will handle the integration with Mastra.ai agents. This module will:

1. Initialize and configure Mastra.ai agents
2. Provide functions to process HTML content through agents
3. Return structured results that can be used by the main crawler

## 3. Required Dependencies

To implement the Mastra.ai agent integration, we'll need the following dependencies:

```
# Existing dependencies
requests>=2.28.0
beautifulsoup4>=4.11.0

# New dependencies for Mastra.ai integration
mastra-ai>=1.0.0  # Core Mastra.ai package
openai>=1.0.0     # Required for OpenAI model access
```

## 4. Implementation Approach

### Step 1: Add Mastra.ai Agent Module

Create a new file `crawler/mastra_agent.py` with the following components:

- Agent configuration and initialization functions
- Content processing functions using Mastra.ai agents
- Helper utilities for processing results

### Step 2: Extend WebCrawler Class

Modify the WebCrawler class to incorporate the Mastra.ai agent capabilities:

- Add optional parameters for enabling Mastra.ai agent features
- Integrate agent content processing in the crawl method
- Store additional structured data extracted by agents

### Step 3: Update CLI Interface

Enhance the command-line interface to support Mastra.ai agent options:

- Add flags for enabling/disabling agent features
- Add options for configuring agent behavior
- Support output of agent-processed data

## 5. Example Code Snippets

### Mastra Agent Module

```python
#!/usr/bin/env python3
from mastra.core import Agent
from mastra.ai_sdk import openai

class ContentAgent:
    def __init__(self, model_name="gpt-4o-mini"):
        """
        Initialize a Mastra.ai agent for content processing
        
        Args:
            model_name (str): The name of the model to use
        """
        self.agent = Agent({
            "name": "ContentProcessingAgent",
            "instructions": "You are a web content analysis agent that extracts key information from web pages.",
            "model": openai(model_name),
        })
    
    def extract_structured_data(self, html_content, url):
        """
        Extract structured data from HTML content
        
        Args:
            html_content (str): The HTML content to analyze
            url (str): The URL where the content was fetched from
            
        Returns:
            dict: Structured data extracted from the content
        """
        result = self.agent.generate([
            {
                "role": "user", 
                "content": f"Extract key information from this web page at {url}:\n\n{html_content[:5000]}..."
            }
        ], {
            "output": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "main_content": {"type": "string"},
                    "topics": {"type": "array", "items": {"type": "string"}},
                    "key_entities": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["title", "main_content", "topics", "key_entities"]
            }
        })
        
        return result.object
```

### Extended WebCrawler Class

```python
# Add to crawler.py

def __init__(self, delay=1, use_mastra_agent=False):
    """
    Initialize the web crawler
    
    Args:
        delay (int): Delay between requests in seconds
        use_mastra_agent (bool): Whether to use Mastra.ai agent for content processing
    """
    self.delay = delay
    self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    self.visited_urls = set()
    self.use_mastra_agent = use_mastra_agent
    
    # Initialize Mastra agent if enabled
    if self.use_mastra_agent:
        from crawler.mastra_agent import ContentAgent
        self.content_agent = ContentAgent()

# Modified crawl method to include agent processing
def crawl(self, start_url, max_pages=10):
    """
    Start crawling from a given URL
    
    Args:
        start_url (str): URL to start crawling from
        max_pages (int): Maximum number of pages to crawl
        
    Returns:
        dict: Dictionary with URLs as keys and content as values
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
            # Process with Mastra agent if enabled
            if self.use_mastra_agent:
                processed_content = self.content_agent.extract_structured_data(html, url)
                results[url] = {
                    "html": html,
                    "processed_content": processed_content
                }
            else:
                # Store the result without processing
                results[url] = html
            
            # Wait before the next request
            time.sleep(self.delay)
    
    return results
```

### CLI Interface Update

```python
# Update to main() function in crawler.py

def main():
    parser = argparse.ArgumentParser(description='Basic Web Crawler')
    parser.add_argument('url', help='URL to start crawling from')
    parser.add_argument('--max-pages', type=int, default=10, help='Maximum number of pages to crawl')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds')
    parser.add_argument('--output-dir', default='./output', help='Directory to save output files')
    parser.add_argument('--use-mastra-agent', action='store_true', help='Use Mastra.ai agent for content processing')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize crawler
    crawler = WebCrawler(delay=args.delay, use_mastra_agent=args.use_mastra_agent)
    
    # Start crawling
    results = crawler.crawl(args.url, max_pages=args.max_pages)
    
    # Save the results
    for i, (url, content) in enumerate(results.items()):
        if args.use_mastra_agent:
            # Save processed content
            filename = f"{i+1}_{urlparse(url).netloc.replace('.', '_')}_processed.json"
            filepath = os.path.join(args.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content["processed_content"], f, indent=2)
            
            # Save HTML content
            html_filename = f"{i+1}_{urlparse(url).netloc.replace('.', '_')}.html"
            html_filepath = os.path.join(args.output_dir, html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(content["html"])
            
            print(f"Saved processed content: {filepath}")
            print(f"Saved HTML content: {html_filepath}")
        else:
            filename = f"{i+1}_{urlparse(url).netloc.replace('.', '_')}.html"
            filepath = os.path.join(args.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Saved: {filepath}")
    
    print(f"Crawling complete. Visited {len(crawler.visited_urls)} pages.")
```

## 6. Next Steps

After implementing this design, the next steps would be:

1. Create a Mastra agent configuration module that handles authentication and setup
2. Implement the full crawler-agent integration with the features described above
3. Create examples and update documentation to show users how to leverage Mastra.ai agents with the crawler

## 7. Limitations and Considerations

- This integration focuses on content processing and not on using agents for crawling decisions
- The integration will require users to have appropriate Mastra.ai API credentials
- Agent processing may add latency to the crawling process
- Large HTML documents might need to be chunked before processing by the agent

## 8. Conclusion

This design provides a clear roadmap for integrating Mastra.ai agents with the existing crawler implementation. By focusing on content processing capabilities, we're keeping the integration simple while still providing valuable AI-powered features. The modular approach ensures that the integration can be extended in the future to include additional agent capabilities.