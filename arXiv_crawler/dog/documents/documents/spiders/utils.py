main_url = 'https://arxiv.org/list/cs/'

# example url:
# https://arxiv.org/list/cs/1901?skip=0&show=100

def gen_years(start, end):
    return list(range(start, end + 1))

def gen_date(year, month):
    year = str(year)[-2:]
    month = str(month)
    if len(month) == 1:
        month = '0' + month
    return year + month

def gen_urls(year, month, num_entries, show=200):
    global main_url

    skips = list(range(0, num_entries, show))
    return [ main_url + str(gen_date(year, month)) +
            '?skip=' + str(skip)  + '&show=' + str(show)
            for skip in skips]

print(gen_urls(2010, 1, 421))
