import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbScrapItem
from fake_useragent import UserAgent

class FilmSpider(CrawlSpider):
    name = "film"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    
    film_details = LinkExtractor(restrict_css='.titleColumn > a')
    rule_film_details = Rule(film_details,
                             callback='parse_item',
                             follow=False,
                             )
    rules = (rule_film_details,)
    

    user_agent = UserAgent().random

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        # all_responses = response.css('.titleColumn a')
        # items = ImdbItem()
        yield {
        # for response in all_responses:
        'titre' :  response.css('.sc-afe43def-1.fDTGTb::text').extract(),
        'titre_original' : response.css('.sc-afe43def-3.EpHJp::text').extract(),
        'score' : response.css('.sc-bde20123-1.iZlgcd::text').extract_first(),
        'genre' : response.css('.ipc-chip__text::text').extract(),
        'annee' : response.css('.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color::text').extract_first().strip('()'),
        'duree': response.css('.ipc-inline-list__item::text').extract_first(),
        'descriptions' : response.css('.sc-5f699a2-1.cfkOAP::text').extract_first().strip(),
        'acteurs' : response.xpath("(//li[@data-testid='title-pc-principal-credit'])[last()]//a/text()")[1:].extract(),
        'public' : response.css('.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color::text').extract_first(),
        'pays' : response.css('.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text').extract()[-1].strip(),
        'langue' : response.css('.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text').extract()[0].strip().strip('()')
        }