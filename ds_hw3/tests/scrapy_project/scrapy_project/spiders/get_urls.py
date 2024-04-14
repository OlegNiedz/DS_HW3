import scrapy
import re


class GetUrlsSpider(scrapy.Spider):
    name = "get_urls"
    allowed_domains = ["index.minfin.com.ua"]
    start_urls = ["https://index.minfin.com.ua/ua/russian-invading/casualties"]

    def parse(self, response,**kwargs):
        content = response.xpath("//div[@class='ajaxmonth']/h4[@class='normal']/a")
        prefix = "/month.php?month="  # month.php?month=2023-09
        for link in content:
            yield {
                "href":prefix + re.search(pattern=r"\d{4}-\d{2}", string=link.xpath('@id').get()).group()
            }

