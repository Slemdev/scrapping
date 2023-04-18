
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbScrapItem
from fake_useragent import UserAgent

# class GetTopMoviesSpider(scrapy.Spider):
#     name = "get_top_movies"
#     allowed_domains = ["imdb.com"]
#     start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

#     def parse(self, response):
#         items = ImdbScrapItem()
#         all_movies = response.css(".lister-list tr")
        
#         for movie in all_movies:
#             title = response.css(".titleColumn a::text").extract()
#             casting = response.css(".titleColumn a::attr(title)").extract()
#             rating = response.css(".ratingColumn.imdbRating strong::text").extract()
#             link = movie.css("a::attr(href)").extract_first()
            
#             items['title'] = title
#             items['casting'] = casting
#             items['rating'] = rating
#             items['link'] = link
            
#             yield items
#             pass
        

class GetTopMoviesSpider(CrawlSpider):
    name = "crawler_get_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    
    user_agent = UserAgent().random
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths=('.titleColumn > a')), callback="parse_item", follow=False),
    )

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        #all_movies = response.css(".titleColumn a")
        
        #for movie in all_movies:
            #items = ImdbScrapItem()
            title = response.css(".title_wrapper h1::text").extract_first()
            casting = response.css(".credit_summary_item a::text").extract()
            rating = response.css(".ratingValue strong span::text").extract_first()
            description = response.css(".summary_text::text").extract_first()
            year = response.css(".title_wrapper a::text").extract_first()
            genre = response.css(".subtext a::text").extract()
            duration = response.css(".subtext time::text").extract_first()
            # casting = movie.css("ipc-metadata-list-item__content-container").extract_first()
            # rating = movie.css("sc-bde20123-1").extract_first()
    
            
            #items['title'] = title
            # items['casting'] = casting
            # items['rating'] = rating
            #items['link'] = link
            
            yield {"title": title, "casting": casting, "rating": rating, "description": description, "year": year, "genre": genre, "duration": duration}