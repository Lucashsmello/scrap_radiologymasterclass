import scrapy
import re
from ..items import CaseItem


class CaseSpider(scrapy.Spider):
    name = "case"

    def start_requests(self):
        urls = [
            'https://www.radiologymasterclass.co.uk/gallery/trauma/x-ray_arm_2/fractures_1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=CaseSpider.parse_case)

    @staticmethod
    def parse_case(response: scrapy.http.HtmlResponse,
                   gallery_name2=None):
        main_content_node = response.xpath('//main[@id="content"]')
        image_classes = main_content_node.xpath('.//figure//a[contains(@class, "imageswap_")]/@class').getall()
        assert len(image_classes) > 0, "No images found in the page {}"

        style_str = response.xpath('//style').extract()[0]
        imageclasses_names_fromstyle = re.findall(r"a\.(imageswap_\d+)", style_str)
        images_urls = re.findall(r"url\((.*?)\)", style_str)

        figcap_node = main_content_node.xpath('.//figcaption')
        figs_caption = [x.xpath('.//h4/text()').getall()[0] for x in figcap_node]
        figs_description = [x.xpath('.//li/text()').getall() for x in figcap_node]
        assert len(figs_description) == len(figs_caption), "Number of captions and descriptions is different"
        assert len(figs_description) == len(images_urls), \
            f"Number of images ({len(images_urls)}) and descriptions ({len(figs_description)}) is different"

        # merge all together in a dict of dicts, where the keys are the imageswap names
        image_data = {}
        for i in range(len(image_classes)):
            image_data[image_classes[i]] = {
                'caption': figs_caption[i],
                'description': figs_description[i],
            }
        for i in range(len(imageclasses_names_fromstyle)):
            image_data[imageclasses_names_fromstyle[i]]['url'] = images_urls[i]

        gallery_name1 = response.url.split('/')[-2]

        case_id = '/'.join(response.url.split('/')[-3:])

        # yield the CaseItems from each image_data
        for _, data in image_data.items():
            yield CaseItem(
                image_urls=[data['url']],
                fig_caption=data['caption'],
                fig_description=data['description'],
                gallery_name1=gallery_name1,
                gallery_name2=gallery_name2,
                case_id=case_id,
            )

        # self.log(f'Saved file {filename}')
