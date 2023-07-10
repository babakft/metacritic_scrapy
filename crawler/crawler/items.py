import scrapy


class MovieItem(scrapy.Item):
    Title = scrapy.Field()
    USER_SCORE = scrapy.Field()
    Runtime = scrapy.Field()
    Languages = scrapy.Field()
    METASCORE = scrapy.Field()
    Genrs = scrapy.Field()
    Countries = scrapy.Field()
    Writers = scrapy.Field()
    PrincipleCast = scrapy.Field()
    Cast = scrapy.Field()
    Director = scrapy.Field()
    url = scrapy.Field()