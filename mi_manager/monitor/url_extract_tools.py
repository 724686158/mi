from tld import get_tld


def extract_main_url(urls):
    res = None
    for i in urls:
        cur = get_tld(i, fail_silently=True)
        if cur:
            res = cur
    return res
