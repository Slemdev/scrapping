import scrapy
from scrapy.spiders import CrawlSpider
from ..items import ImdbScrapItem


# class CrawlerGetTopMoviesSpider(CrawlSpider):
#     name = 'crawler_get_top_movies'
#     allowed_domains = ['imdb.com']
#     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

#     def start_requests(self):
#         yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
#             'User-Agent': self.user_agent
#         })

#     def parse(self, response):
#         all_movies = response.css(".lister-list tr")

#         for movie in all_movies:
#             items = ImdbScrapItem()
#             title = movie.css(".titleColumn a::text").extract()
#             casting = movie.css(".titleColumn a::attr(title)").extract()
#             rating = movie.css(".ratingColumn.imdbRating strong::text").extract()
#             link = movie.css("a::attr(href)").extract_first()

#             items['title'] = title
#             items['casting'] = casting
#             items['rating'] = rating
#             items['link'] = link

#             yield items
#             pass

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