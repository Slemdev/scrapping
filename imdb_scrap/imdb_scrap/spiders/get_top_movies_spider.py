import scrapy


class GetTopMoviesSpider(scrapy.Spider):
    name = "get_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        movies = response.css(".titleColumn a::text").extract()
        casting = response.css(".titleColumn a::attr(title)").extract()
        yield {"movies": movies, "casting": casting}
        pass
        

class GetDescriptionTopMoviesSpider(scrapy.Spider):
    name = "get_description_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        descriptions = response.css(".ratingColumn.imdbRating p::text").extract()
        yield {"descriptions": descriptions}
        pass