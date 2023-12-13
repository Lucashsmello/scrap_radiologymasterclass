# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from .items import CaseItem


class ScrapRadiologymasterclassPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CaseItem):
            item.fig_description = '\n'.join(item.fig_description)
        return item


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item: CaseItem = None):
        # just gets the automatically generated path and sets in the item
        path = super().file_path(request, response, info)
        if path.startswith('full/'):
            path = path[5:]
        item.file_path = path
        return path
