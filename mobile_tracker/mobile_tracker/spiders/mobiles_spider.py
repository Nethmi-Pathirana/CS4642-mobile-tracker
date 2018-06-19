import scrapy

class MobileSpider(scrapy.Spider):
    name = "mobile_phones"

    start_urls = ['https://ikman.lk/en/ads/matara/mobile-phones?categoryType=ads&categoryName=Electronics']

    def parse(self, response):
        # follow links to mobile pages
        for href in response.css('div.item-content a::attr(href)'):
            yield response.follow(href, self.parse_mobile)

        # follow pagination links
        for href in response.css('a.pag-next::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_mobile(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        arr_attribute = response.css('div.item-properties dt::text').extract()
        arr_value = response.css('div.item-properties dd::text').extract()
        print arr_attribute
        print arr_value
        item_properties ={}
        for i in range(0, len(arr_attribute)):
            item_properties[arr_attribute[i]] = arr_value[i]

        def check_attribute(property):
            value = ''
            if property in item_properties.keys():
                value = item_properties[property]
            return value

        yield {
            'mobile_name': extract_with_css('div.item-top h1::text'),
            'sale_by': extract_with_css('p.item-intro span.poster::text'), #use regular expressions to split
            'date': extract_with_css('p.item-intro span.date::text'),
            'location': extract_with_css('p.item-intro span.location::text'),
            'condition': check_attribute("Condition:"),
            'brand': check_attribute("Brand:"),
            'model': check_attribute("Model:"),
            'edition': check_attribute("Edition:"),
            'authenticity': check_attribute("Authenticity:"),
	        'price': extract_with_css('div.ui-price-tag span.amount::text'),
            'features': check_attribute("Features:"),
            'description': response.css('div.item-description p::text').extract(),
        }
