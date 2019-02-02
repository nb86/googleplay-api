from config import SEPARATOR

def sizeof_fmt(num):
    num = int(num)
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0

def print_header_line():
    l = [ "Title",
                "Package name",
                "Creator",
                "Price",
                "Offer Type",
                "Version Code",
                "Size",
                "Rating",
                "Num Downloads",
             ]
    print(SEPARATOR.join(l))

def print_result_line(c):
    #c.offer[0].micros/1000000.0
    #c.offer[0].currencyCode
    l = [ c['title'],
                c['docid'],
                c['creator'],
                c['offer'][0]['formattedAmount'],
                c['offer'][0]['offerType'],
                c['details']['appDetails']['versionCode'],
                sizeof_fmt(c['details']['appDetails']['installationSize']),
                "%.2f" % c['aggregateRating']['starRating'],
                c['details']['appDetails']['numDownloads']]
    print(SEPARATOR.join(str(i) for i in l))

