import time

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from crawler.items import MovieItem


class MetatricSpider(CrawlSpider):
    name = "metatric"
    allowed_domains = ["metacritic.com"]
    start_urls = ["https://www.metacritic.com/browse/movies/score/metascore/all"]
    custom_setting = {
        'ITEM_PIPELINES': {
             "crawler.pipelines.SaveData": 300,
        }
    }
    rules = [
        Rule(LinkExtractor(allow='/movie/', deny=('/user-reviews', '/critic-reviews')),
             callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_css='a.action'), follow=True)
    ]

    def parse_item(self, response):
        complete_url = response.url + '/details'

        with open('crawled_link.txt', 'r') as crawled_link:
            for link in crawled_link:
                if link.rstrip('\n') == complete_url:
                    return
        yield scrapy.Request(url=complete_url, callback=self.get_full_data)

    def get_full_data(self, response):
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
