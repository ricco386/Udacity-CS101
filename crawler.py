#Finish crawl web

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index



# Indexing
def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            for element in entry:
                if element[0] == url:
                    return
            entry[1].append([url, 0])
            return
    index.append([keyword, [[url, 0]]])

def lookup(index,keyword):
    for entry in index:
        if entry[0] == keyword:
        return entry[1]
    return []

def add_page_to_index(index,url,content):
    words = content.split()
    for keyword in words:
        add_to_index(index,keyword,url)

def record_user_click(index,keyword,url):
    urls = lookup(index, keyword)
        if urls:
            for entry in urls:
                if entry[0] == url:
                    entry[1] += 1

print crawl_web('http://xkcd.com/353')
