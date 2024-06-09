import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
from app.utils.file_utils import load_matrix, save_matrix

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def start_requests(self):
        matrix = load_matrix()
        
        for chapter in matrix["chapters"]:
            for result in chapter["search_results"]:
                yield scrapy.Request(url=result['url'], callback=self.parse, meta={'chapter_title': chapter['title']})

    def parse(self, response):
        chapter_title = response.meta['chapter_title']
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.get_text()

        matrix = load_matrix()
        for chapter in matrix["chapters"]:
            if chapter["title"] == chapter_title:
                chapter["scraped_content"] += main_content

        save_matrix(matrix)

def run_scrapy_spider():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(ContentSpider)
    process.start()
