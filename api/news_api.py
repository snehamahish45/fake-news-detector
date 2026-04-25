import feedparser

def get_news(category="general"):
    feeds = {
        "general": "http://feeds.bbci.co.uk/news/rss.xml",
        "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
        "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "sports": "http://feeds.bbci.co.uk/sport/rss.xml"
    }

    url = feeds.get(category, feeds["general"])
    feed = feedparser.parse(url)

    news_list = []
    for entry in feed.entries[:10]:
        news_list.append((entry.title, entry.link))

    return news_list