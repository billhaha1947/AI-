import feedparser
import time
from bs4 import BeautifulSoup

# Nguồn RSS theo chủ đề mà m chọn: công nghệ, game, xã hội, trend
FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.polygon.com/rss/index.xml",
    "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "https://cointelegraph.com/rss",
    "https://www.espn.com/espn/rss/news"
]

def clean(html):
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text()

def fetch_news_from_feeds(limit=10):
    items = []
    for url in FEEDS:
        d = feedparser.parse(url)
        source = d.feed.get("title", url)
        for e in d.entries[:5]:
            items.append({
                "title": e.title,
                "link": e.link,
                "summary": clean(e.get("summary", "")),
                "ts": int(time.time())
            })
    items.sort(key=lambda x: x["ts"], reverse=True)
    return items[:limit]
