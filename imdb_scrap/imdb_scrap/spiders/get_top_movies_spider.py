import scrapy


class GetTopMoviesSpider(scrapy.Spider):
    name = "get_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        movies = response.css(".titleColumn a::text").extract()
        casting = response.css(".titleColumn a::attr(title)").extract()
        rating = response.css(".ratingColumn.imdbRating strong::text").extract()
        links = response.css(".titleColumn a::attr(href)").extract()
        yield {"movies": movies, "casting": casting, "rating": rating, "links": links}
        pass