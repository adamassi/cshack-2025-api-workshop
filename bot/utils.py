from firecrawl import FirecrawlApp, ScrapeOptions

class MyFirecrawlApp:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.app = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> str:
        return self.app.scrape_url(url, formats=['markdown'])

