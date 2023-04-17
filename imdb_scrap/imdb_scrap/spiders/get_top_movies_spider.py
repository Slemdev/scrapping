import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbScrapItem


class CrawlerGetTopMoviesSpider(CrawlSpider):
    name = 'crawler_get_top_movies'
    allowed_domains = ['imdb.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]',)), callback="parse_item", follow=True),
    )

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        items = ImdbScrapItem()
        title_xpath = './/td[@class="titleColumn"]/a/text()'
        year_xpath = './/td[@class="titleColumn"]/span[@class="secondaryInfo"]/text()'
        casting_xpath = './/td[@class="titleColumn"]/a[@title]/@title'
        rating_xpath = './/td[@class="ratingColumn imdbRating"]/strong/text()'
        
        title = response.xpath(title_xpath).get()
        year = response.xpath(year_xpath).get()
        casting = response.xpath(casting_xpath).get()
        rating = response.xpath(rating_xpath).get()
        
        items['title'] = title
        items['year'] = year
        items['casting'] = casting
        items['rating'] = rating
        
        yield items


class GetTopMoviesSpider(scrapy.Spider):
    name = "get_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        items = ImdbScrapItem()
        all_movies = response.css(".lister-list tr")
        
        for movie in all_movies:
            title = response.css(".titleColumn a::text").extract()
            casting = response.css(".titleColumn a::attr(title)").extract()
            rating = response.css(".ratingColumn.imdbRating strong::text").extract()
            link = movie.css("a::attr(href)").extract_first()
            
            items['title'] = title
            items['casting'] = casting
            items['rating'] = rating
            items['link'] = link
            
            yield items
            pass