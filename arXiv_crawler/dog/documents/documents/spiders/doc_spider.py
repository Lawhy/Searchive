import scrapy


class DogSpider(scrapy.Spider):
    name = "documents"

    def start_requests(self):
        urls = [
            'https://arxiv.org/abs/1901.00004',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        x_title = '//div[@id="content"]/div[@id="abs"]/h1[@class="title mathjax"]/text()'
        x_authors = '//div[@id="content"]/div[@id="abs"]/div[@class="authors"]/a/text()'
        x_abstract = '//div[@id="content"]/div[@id="abs"]/blockquote[@class="abstract mathjax"]/text()'
        x_primary_subject = '//td[@class="tablecell subjects"]/span[@class="primary-subject"]/text()'
        x_subjects = '//td[@class="tablecell subjects"]/text()'

        title = response.xpath(x_title).extract()
        authors = response.xpath(x_authors).extract()
        abstract = response.xpath(x_abstract).extract()
        primary_subject = response.xpath(x_primary_subject).extract()
        subjects = response.xpath(x_subjects).extract()

        # determine whether or not there are secondary subjects
        has_secondary = not len(subjects) == 1
        if has_secondary:
            subjects = primary_subject + [sub.replace('; ', '') for sub in subjects[1:]]

        yield {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "primary_subject": primary_subject,
            "subjects": subjects
        }
