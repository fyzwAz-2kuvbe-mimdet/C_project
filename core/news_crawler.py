import re
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; SM-G975U) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Mobile Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://m.naver.com/",
}


def search_news(query: str, max_results: int = 10) -> list:
    items = _fetch_mobile(query, max_results)
    if not items:
        items = _fetch_pc(query, max_results)
    return items


# ── mobile (더 안정적) ──

def _fetch_mobile(query: str, max_results: int) -> list:
    url = f"https://m.search.naver.com/search.naver?where=m_news&query={quote(query)}&sort=1"
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        articles = (
            soup.select("div.news_section li")
            or soup.select("ul.lst_news li")
            or soup.select("div.group_news li")
            or soup.select("li.bx")
        )

        items = []
        for tag in articles[:max_results]:
            item = _parse_mobile(tag)
            if item:
                items.append(item)
        return items
    except Exception:
        return []


def _parse_mobile(tag) -> dict | None:
    a = (
        tag.select_one("a.news_tit")
        or tag.select_one("a.tit")
        or tag.select_one("a[class*='tit']")
        or tag.select_one("strong a")
        or tag.select_one("a")
    )
    if not a:
        return None

    headline = a.get_text(strip=True)
    link = a.get("href", "")
    if not headline or not link or link.startswith("#"):
        return None

    press_tag = tag.select_one("span.press") or tag.select_one("a.press") or tag.select_one("span[class*='press']")
    press = press_tag.get_text(strip=True) if press_tag else ""

    date_tag = tag.select_one("span.date") or tag.select_one("span[class*='date']") or tag.select_one("span.time")
    raw_date = date_tag.get_text(strip=True) if date_tag else ""

    summary_tag = tag.select_one("div.dsc") or tag.select_one("span.dsc") or tag.select_one("div[class*='dsc']")
    summary = summary_tag.get_text(strip=True) if summary_tag else ""

    return {
        "headline": headline,
        "link": link,
        "press": press,
        "date": _normalize_date(raw_date),
        "summary": summary[:200] + "..." if len(summary) > 200 else summary,
    }


# ── PC fallback ──

def _fetch_pc(query: str, max_results: int) -> list:
    url = f"https://search.naver.com/search.naver?where=news&query={quote(query)}&sort=1"
    headers = {**_HEADERS, "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        articles = (
            soup.select("div.news_wrap")
            or soup.select("div.news_area")
            or soup.select("ul.list_news li")
            or soup.select("li.bx")
        )

        items = []
        for tag in articles[:max_results]:
            item = _parse_pc(tag)
            if item:
                items.append(item)
        return items
    except Exception:
        return []


def _parse_pc(tag) -> dict | None:
    a = (
        tag.select_one("a.news_tit")
        or tag.select_one("a[class*='news_tit']")
        or tag.select_one("a[class*='tit']")
    )
    if not a:
        return None

    headline = a.get_text(strip=True)
    link = a.get("href", "")
    if not headline or not link:
        return None

    press_tag = (
        tag.select_one("a.info.press")
        or tag.select_one("a.press")
        or tag.select_one("span.press")
    )
    press = press_tag.get_text(strip=True) if press_tag else ""

    date_tag = tag.select_one("span.info") or tag.select_one("span[class*='date']")
    raw_date = date_tag.get_text(strip=True) if date_tag else ""

    summary_tag = tag.select_one("div.dsc_wrap") or tag.select_one("div[class*='dsc']")
    summary = summary_tag.get_text(strip=True) if summary_tag else ""

    return {
        "headline": headline,
        "link": link,
        "press": press,
        "date": _normalize_date(raw_date),
        "summary": summary[:200] + "..." if len(summary) > 200 else summary,
    }


def _normalize_date(raw: str) -> str:
    m = re.search(r"\d{4}\.\d{2}\.\d{2}", raw)
    if m:
        return m.group(0).replace(".", "-").rstrip("-")
    return raw or "날짜 미상"
