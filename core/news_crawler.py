import re
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def search_news(query: str, max_results: int = 10) -> list:
    encoded = quote(query)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded}&sort=1"

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Try several container selectors Naver has used over the years
    containers = (
        soup.select("div.news_wrap.api_ani_send")
        or soup.select("div.news_area")
        or soup.select("li.bx")
        or soup.select("div[class*='news_wrap']")
    )

    items = []
    for container in containers[:max_results]:
        try:
            item = _parse(container)
            if item:
                items.append(item)
        except Exception:
            continue

    return items


def _parse(tag) -> dict | None:
    title_tag = (
        tag.select_one("a.news_tit")
        or tag.select_one("a.title")
        or tag.select_one("a[class*='tit']")
    )
    if not title_tag:
        return None

    headline = title_tag.get_text(strip=True)
    link = title_tag.get("href", "")
    if not headline or not link:
        return None

    press_tag = (
        tag.select_one("a.info.press")
        or tag.select_one("a.press")
        or tag.select_one("span.press")
        or tag.select_one("a[class*='press']")
    )
    press = press_tag.get_text(strip=True) if press_tag else "알 수 없음"

    date_tag = (
        tag.select_one("span.info")
        or tag.select_one("span.date")
        or tag.select_one("span[class*='date']")
    )
    raw_date = date_tag.get_text(strip=True) if date_tag else ""
    date = _normalize_date(raw_date)

    summary_tag = (
        tag.select_one("div.dsc_wrap")
        or tag.select_one("div.api_txt_lines")
        or tag.select_one("div[class*='dsc']")
    )
    summary = summary_tag.get_text(strip=True) if summary_tag else ""
    if len(summary) > 200:
        summary = summary[:200] + "..."

    return {"headline": headline, "link": link, "press": press, "date": date, "summary": summary}


def _normalize_date(raw: str) -> str:
    m = re.search(r"\d{4}\.\d{2}\.\d{2}", raw)
    if m:
        return m.group(0).replace(".", "-").rstrip("-")
    return raw or "날짜 미상"
