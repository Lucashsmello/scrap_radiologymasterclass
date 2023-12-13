import scrapy
from .case_spider import CaseSpider


class GallerySpider(scrapy.Spider):
    name = 'gallery'

    def start_requests(self):
        urls = [
            'https://www.radiologymasterclass.co.uk/gallery/galleries',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.HtmlResponse):
        div_nodes = response.xpath('//div[@class="text_width"]')
        gallery_name2 = div_nodes.xpath('.//h2/text()').getall()
        urls = [gallery_section.xpath('.//li//@href').getall()
                for gallery_section in div_nodes.xpath('.//div[@class="gallinfo"]')]
        assert len(gallery_name2) == len(urls), "Number of gallery sections is different from number of gallery names"

        for galleries_urls, name in zip(urls, gallery_name2):
            if 'CT Brain' in name:
                continue
            for url in galleries_urls:
                yield response.follow(url=url, callback=self.parse_gallery,
                                      cb_kwargs={'gallery_name2': name})

    def parse_gallery(self, response: scrapy.http.HtmlResponse,
                      gallery_name2=None):
        yield from CaseSpider.parse_case(response,
                                         gallery_name2=gallery_name2)

        urls = response.xpath('//div[@class="content-wrapper"]/nav//li/a/@href').getall()
        assert len(urls) > 1
        for url in urls:
            if url.startswith('/gallery'):
                continue
            if url.strip() == '/':
                continue

            # Use CaseSpider to parse the url
            yield response.follow(url=url, callback=CaseSpider.parse_case,
                                  cb_kwargs={'gallery_name2': gallery_name2})
