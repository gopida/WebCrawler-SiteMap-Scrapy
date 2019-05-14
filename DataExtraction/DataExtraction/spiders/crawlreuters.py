import scrapy
import datetime
from scrapy.spiders import SitemapSpider
from DataExtraction.items import ExtractnewsarticlesItem
from DataExtraction.util import getDateTime
from datetime import datetime as dt


class SpiderReuters(SitemapSpider):
    name = 'reuters-spider'
    delta = 2
    sitemap_urls = []
    today = dt.now()
    startDate = today - datetime.timedelta(days=delta)

    for x in range(0, delta):

        start = startDate.strftime('%Y%m%d')
        endDate = startDate + datetime.timedelta(days=1)
        end = endDate.strftime('%Y%m%d')
        str = 'https://www.reuters.com/sitemap_{}-{}.xml'.format(start, end)
        print("xml url ", str)
        sitemap_urls.append(str)
        startDate = endDate

    sitemap_rules = [
        ('/article/', 'parse_article_urls'),
        ('', 'parse')
    ]
    address_list = []

    def parse(self, response):
        print("default parsing method for {}".format(response.url))

    def parse_article_urls(self, response):
        print("parse article method for {}".format(response.url))
        yield scrapy.Request(response.url, callback=self.parse_article, dont_filter=True)

    def parse_article(self, response):
        address = response.request.url
        if address not in self.address_list:
            self.address_list.append(address)
            item = ExtractnewsarticlesItem()
            item['address'] = address
            item['title'] = response.css('h1.ArticleHeader_headline::text').extract()
            article = response.css('div.StandardArticleBody_body > p::text').extract()
            if not article:
                article = response.css('div.StandardArticleBody_body > div >  pre::text').extract()
            unformatted_time = response.css('div.ArticleHeader_date::text').extract()
            item['datetime'] = getDateTime(unformatted_time[0])
            item['content'] = "".join(str(data) for data in article).encode('utf8')
            yield item

