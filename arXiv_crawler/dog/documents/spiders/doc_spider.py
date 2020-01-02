import scrapy
import re

def transform_number(num):
    # the arxiv number only accepts NNNNN (5 digits), which means from 00000 to 99999
    num_zeros = 5 - len(str(num))
    return (num_zeros * "0") + str(num)

def gen_urls(time):
    main_url = 'https://export.arxiv.org/abs/'
    # the format of time is yymm, e.g. 1901
    return [main_url + str(time) + '.' + transform_number(num) for num in range(0, 15000)]

def read_id(url):
    return re.findall('https://export.arxiv.org/abs/(.+)', url)[0]

class DogSpider(scrapy.Spider):
    name = "documents"

    def start_requests(self):
        urls = gen_urls(1902)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        x_title = '//div[@id="abs"]/div[@class="leftcolumn"]/h1[@class="title mathjax"]/text()'
        x_authors = '//div[@id="abs"]/div[@class="leftcolumn"]/div[@class="authors"]/a/text()'
        x_abstract = '//div[@id="abs"]/div[@class="leftcolumn"]/blockquote[@class="abstract mathjax"]/text()'
        x_primary_subject = '//td[@class="tablecell subjects"]/span[@class="primary-subject"]/text()'
        x_subjects = '//td[@class="tablecell subjects"]/text()'

        title = response.xpath(x_title).extract()
        authors = response.xpath(x_authors).extract()
        abstract = response.xpath(x_abstract).extract()[1:]  # by inspection, the first element is '\n'
        primary_subject = response.xpath(x_primary_subject).extract()
        subjects = response.xpath(x_subjects).extract()

        # determine whether or not there are secondary subjects
        if subjects == []:
            subjects = primary_subject
        else:
            subjects = primary_subject + subjects[0].split('; ')[1:] # by inspection the first element is always empty

        # if there is no title for the current number, meaning that no further documents
        if title == []:
            raise CloseSpider('valid number exceeded')

        yield {
            "id": read_id(response.request.url),
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "primary_subject": primary_subject,
            "subjects": subjects
        }
