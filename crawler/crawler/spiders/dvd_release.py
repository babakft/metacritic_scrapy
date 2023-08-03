import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from crawler.items import MovieItem


class DvdReleaseSpider(CrawlSpider):
    name = "dvd_release"
    allowed_domains = ["www.metacritic.com"]
    start_urls = ["https://www.metacritic.com/browse/dvds/release-date/new-releases/date"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "crawler.pipelines.UpdateData": 300},
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 0.2

    }
    rules = [Rule(LinkExtractor(allow='/movie/', deny=('/user-reviews', '/critic-reviews')),
                  callback="parse_item", follow=False)]

    def parse_item(self, response):
        """the full data url is a little different"""
        yield scrapy.Request(url=response.url + '/details', callback=self.get_full_data)

    @staticmethod
    def get_full_data(response):
        details = MovieItem()
        details['Title'] = response.css('h1::text').extract_first()
        details['USER_SCORE'] = response.css('a.metascore_anchor > span::text').extract()[1]
        details['METASCORE'] = response.css('a.metascore_anchor > span::text').extract()[0]
        details['Runtime'] = response.css('tr.runtime > td.data::text').extract_first()
        details['Languages'] = response.css('tr.languages > td.data > span::text').extract()
        details['Genrs'] = response.css('tr.genres > td.data > span::text').extract()
        details['Countries'] = response.css('tr.countries > td.data > span::text').extract()
        details['Director'] = [director.strip() for director in
                               response.css(
                                   'div.credits_list table:nth-child(1) > tbody > tr > td > a::text ').extract()]
        details['Writers'] = [writer.strip() for writer in
                              response.css(
                                  'div.credits_list table:nth-child(2) > tbody > tr > td > a::text ').extract()]
        details['PrincipleCast'] = [principle.strip() for principle in
                                    response.css(
                                        'div.credits_list table:nth-child(3) > tbody > tr > td > a::text ').extract()]
        details['Cast'] = [cast.strip() for cast in
                           response.css('div.credits_list table:nth-child(4) > tbody > tr > td > a::text ').extract()]
        details['url'] = response.url

        return details
