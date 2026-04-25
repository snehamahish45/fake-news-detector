import feedparser

def get_news(category="general"):
    feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.skynews.com/feeds/rss/home.xml"
    ]

    news_list = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            news_list.append((entry.title, entry.link))

    return news_list