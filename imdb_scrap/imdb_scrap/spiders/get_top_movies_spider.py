import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbScrapItem
from fake_useragent import UserAgent

        
class GetTopMoviesSpider(CrawlSpider):
    name = "crawler_get_top_movies"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    
    user_agent = UserAgent().random
    
    rules = (
        Rule(LinkExtractor(restrict_css='.titleColumn > a'), callback="parse_item", follow=False),
    )

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', 
                             headers={
                                'User-Agent': self.user_agent
                            }
        )

    def parse_item(self, response):
        items = ImdbScrapItem()
        
        #items['title'] = response.css('.sc-52d569c6-0.kNzJA-D.sc-afe43def-3.EpHJp::text').extract_first()
        items['original_title'] = response.css(".sc-afe43def-0.hnYaOZ span::text").extract()
        items['rating'] = response.css(".sc-bde20123-1.iZlgcd::text").extract_first()
        items['genre'] = response.css(".ipc-chip__text::text").extract()
        items['duration'] = response.css(".ipc-inline-list__item::text").extract_first()
        items['description'] = response.css(".sc-5f699a2-1.cfkOAP::text").extract_first().strip()
        items['casting'] = response.css('li[data-testid="title-pc-principal-credit"]:last-child a::text')[1:].extract()
        items['year'] = response.xpath("(//div[@class='sc-52d569c6-0 kNzJA-D']//li)[1]/a/text()").extract_first()
        
        #items['year'] = response.css('ipc-inline-list.ipc-inline-list--show-dividers.sc-afe43def-4.kdXikI.baseAlt li a::text').extract_first().strip('()')
        #items['public'] = response.css('.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color::text').extract_first()
        #items['country'] = response.css('.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text').extract()[-1].strip()
        #items['language'] = response.css('.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text').extract()[0].strip('()')
        yield items
        
        
class GetTopSeriesSpider(CrawlSpider):
    name = "crawler_get_top_series"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"]
    
    user_agent = UserAgent().random
    
    rules = (
        Rule(LinkExtractor(restrict_css='.titleColumn > a'), callback="parse_item", follow=False),
    )

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', 
                             headers={
                                'User-Agent': self.user_agent
                            }
        )

    def parse_item(self, response):
        items = ImdbScrapItem()
        
        #items['title'] = response.css('.sc-52d569c6-0.kNzJA-D.sc-afe43def-3.EpHJp::text').extract_first()
        items['original_title'] = response.css(".sc-afe43def-0.hnYaOZ span::text").extract()
        items['rating'] = response.css(".sc-bde20123-1.iZlgcd::text").extract_first()
        items['genre'] = response.css(".ipc-chip__text::text").extract()
        items['duration'] = response.css(".ipc-inline-list__item::text").extract_first()
        items['description'] = response.css(".sc-5f699a2-1.cfkOAP::text").extract_first().strip()
        items['casting'] = response.css('li[data-testid="title-pc-principal-credit"]:last-child a::text')[1:].extract()
        items['year'] = response.xpath("(//div[@class='sc-52d569c6-0 kNzJA-D']//li)[2]/a/text()").extract_first()
        
        yield items