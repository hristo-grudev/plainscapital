import scrapy

from scrapy.loader import ItemLoader

from ..items import PlainscapitalItem
from itemloaders.processors import TakeFirst


class PlainscapitalSpider(scrapy.Spider):
	name = 'plainscapital'
	start_urls = ['https://www.plainscapital.com/about/newsroom/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="link "]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="pcb-pagination"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="single-newsroom-contnet-container"]/div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=PlainscapitalItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
