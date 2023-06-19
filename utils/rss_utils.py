import feedparser

def fetch(rss_url):
    """
    抓取rss内容
    """
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries:
        items.append(
            {
            'Title': entry.title,
            'Link': entry.link,
            'Summary': entry.summary,
            'Published': entry.published
            }
        )
    return items
