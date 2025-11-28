"""RSS Feed Collector"""

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

import feedparser

from config.paths import OPML_FILE, ARTICLES_FILE


@dataclass
class Article:
    title: str
    link: str
    summary: str
    source: str
    published: str


def parse_opml(opml_path) -> list[dict]:
    """OPML 파일에서 RSS 피드 URL 추출"""
    tree = ET.parse(opml_path)
    feeds = []
    
    for outline in tree.iter("outline"):
        url = outline.get("xmlUrl")
        if url:
            feeds.append({
                "name": outline.get("text", "Unknown"),
                "url": url
            })
    
    return feeds


def get_collection_period() -> tuple[datetime, datetime]:
    """지난 주 월요일-일요일 기간 계산
    
    예시 (오늘 = 11/28 금요일):
    - today.weekday() = 4 (금요일)
    - last_monday = 11/28 - 11 = 11/17
    - last_sunday = 11/17 + 6 = 11/23
    """
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    # 일요일 23:59:59까지 포함
    last_sunday = last_sunday.replace(hour=23, minute=59, second=59)
    return last_monday, last_sunday


def fetch_feed(url: str, name: str, start_date: datetime, end_date: datetime) -> list[Article]:
    """단일 RSS 피드에서 지정 기간 기사 수집"""
    articles = []
    
    try:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:20]:
            # 발행일 파싱
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            
            # 기간 내 기사만 수집
            if pub_date and start_date <= pub_date <= end_date:
                summary = getattr(entry, "summary", "")[:500]
                articles.append(Article(
                    title=entry.get("title", ""),
                    link=entry.get("link", ""),
                    summary=summary,
                    source=name,
                    published=pub_date.strftime("%Y-%m-%d")
                ))
    except Exception as e:
        print(f"  ⚠️ {name}: {e}")
    
    return articles


def collect_all() -> list[dict]:
    """모든 피드에서 지난 주 기사 수집"""
    feeds = parse_opml(OPML_FILE)
    all_articles = []
    
    start_date, end_date = get_collection_period()
    print(f"📡 {len(feeds)}개 피드에서 수집 중...")
    print(f"📅 수집 기간: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
    
    for feed in feeds:
        articles = fetch_feed(feed["url"], feed["name"], start_date, end_date)
        all_articles.extend(articles)
        if articles:
            print(f"  ✓ {feed['name']}: {len(articles)}개")
    
    # 최신순 정렬
    all_articles.sort(key=lambda x: x.published, reverse=True)
    print(f"\n📰 총 {len(all_articles)}개 기사 수집 완료")
    
    return [asdict(a) for a in all_articles]


def save_articles(articles: list[dict]):
    """수집된 기사를 JSON으로 저장"""
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    articles = collect_all()
    save_articles(articles)