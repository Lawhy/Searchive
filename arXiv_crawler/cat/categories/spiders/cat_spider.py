import scrapy


class CatSpider(scrapy.Spider):
    name = "categories"

    def start_requests(self):
        urls = [
            'https://arxiv.org/archive/cs',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # extract the categories
        cats = response.xpath('//ul/li/b/text()').extract()
        # remove irrelevant terms from cats
        typ = 'cs.'
        cats = [cat.split(' - ') for cat in cats if typ in cat]

        # extract the discriptions
        dess = response.xpath('//ul/li/div[@class="description"]/text()').extract()

        assert len(dess) == len(cats)
        with open('cat_n_des.txt', 'w+', encoding='utf-8') as f:
            for i in range(len(cats)):
                abbr = cats[i][0]
                full = cats[i][1]
                des = dess[i]
                f.write(abbr + '\t' + full + '\t' + des + '\n')
