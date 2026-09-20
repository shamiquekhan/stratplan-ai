from typing import Dict, Any
import httpx
import os
from bs4 import BeautifulSoup
from app.core.config import settings


async def collect_market_data(industry: str) -> Dict[str, Any]:
    result = {"benchmarks": {}, "macro": {}, "fred": {}, "alpha_vantage": {}}
    
    # Collect FRED macro data
    if settings.FRED_API_KEY:
        try:
            fred_data = await _fetch_fred_data()
            result["fred"] = fred_data
            result["macro"] = _parse_fred_macro(fred_data)
        except Exception as e:
            print(f"FRED error: {e}")
    
    # Collect Alpha Vantage industry data
    if settings.ALPHA_VANTAGE_API_KEY:
        try:
            av_data = await _fetch_alpha_vantage_industry(industry)
            result["alpha_vantage"] = av_data
            result["benchmarks"] = _parse_alpha_vantage_benchmarks(av_data)
        except Exception as e:
            print(f"Alpha Vantage error: {e}")
    
    # Add Finnhub market sentiment if available
    if settings.FINNHUB_API_KEY:
        try:
            finnhub_data = await _fetch_finnhub_sentiment(industry)
            result["benchmarks"]["market_sentiment"] = finnhub_data
        except Exception as e:
            print(f"Finnhub error: {e}")
    
    return result


async def _fetch_fred_data() -> Dict[str, Any]:
    series = {
        "GDP_GROWTH": "A191RL1Q225SBEA",
        "CPI": "CPIAUCSL",
        "FED_FUNDS": "FEDFUNDS",
        "UNEMPLOYMENT": "UNRATE",
        "CONSUMER_CONFIDENCE": "UMCSENT"
    }
    
    data = {}
    async with httpx.AsyncClient(timeout=30) as client:
        for name, series_id in series.items():
            url = "https://api.stlouisfed.org/fred/series/observations"
            params = {
                "series_id": series_id,
                "api_key": settings.FRED_API_KEY,
                "file_type": "json",
                "limit": 1,
                "sort_order": "desc"
            }
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                obs = resp.json().get("observations", [])
                if obs:
                    data[name] = float(obs[0]["value"])
    
    return data


def _parse_fred_macro(fred: Dict) -> Dict[str, float]:
    return {
        "gdp_growth": fred.get("GDP_GROWTH", 0.02) / 100,
        "inflation_rate": fred.get("CPI", 3.0) / 100,
        "interest_rate": fred.get("FED_FUNDS", 5.0) / 100,
        "unemployment_rate": fred.get("UNEMPLOYMENT", 4.0) / 100,
        "consumer_confidence": fred.get("CONSUMER_CONFIDENCE", 100)
    }


async def _fetch_alpha_vantage_industry(industry: str) -> Dict[str, Any]:
    sector_map = {
        "saas": "TECHNOLOGY",
        "fintech": "FINANCIAL_SERVICES",
        "healthcare": "HEALTHCARE",
        "ecommerce": "CONSUMER_CYCLICAL",
        "retail": "CONSUMER_CYCLICAL",
        "manufacturing": "INDUSTRIALS",
        "real estate": "REAL_ESTATE",
        "energy": "ENERGY"
    }
    
    sector = sector_map.get(industry.lower(), "TECHNOLOGY")
    
    async with httpx.AsyncClient(timeout=30) as client:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "SECTOR",
            "apikey": settings.ALPHA_VANTAGE_API_KEY
        }
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
    
    return {}


def _parse_alpha_vantage_benchmarks(data: Dict) -> Dict[str, Any]:
    benchmarks = {}
    rank_a = data.get("Rank A: Real-Time Performance", [])
    for item in rank_a:
        if item.get("Sector") == "Technology":
            benchmarks = {
                "avg_growth_rate": float(item.get("1 Year", "0%").replace("%", "")) / 100,
                "avg_margin": float(item.get("Profit Margin", "0%").replace("%", "")) / 100
            }
    return benchmarks


async def _fetch_finnhub_sentiment(industry: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=30) as client:
        url = "https://finnhub.io/api/v1/news-sentiment"
        params = {"token": settings.FINNHUB_API_KEY}
        resp = await client.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
    return {}


async def collect_competitor_data(competitors: str) -> Dict[str, Any]:
    """Scrape competitor websites for pricing, features, tech stack"""
    urls = [c.strip() for c in competitors.split(",") if c.strip()]
    results = {}
    
    for url in urls[:5]:
        try:
            results[url] = await _scrape_competitor(url)
        except Exception as e:
            print(f"Scraping error for {url}: {e}")
            results[url] = {"error": str(e)}
    
    return results


async def _scrape_competitor(url: str) -> Dict[str, Any]:
    from bs4 import BeautifulSoup
    
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        
        return {
            "url": url,
            "title": soup.title.string if soup.title else "",
            "meta_description": soup.find("meta", {"name": "description"}).get("content", "") if soup.find("meta", {"name": "description"}) else "",
            "pricing": _extract_pricing(soup),
            "features": _extract_features(soup),
            "tech_stack": _detect_tech_stack(resp.headers, soup),
            "positioning": _extract_positioning(soup)
        }


def _extract_pricing(soup: BeautifulSoup) -> list:
    pricing = []
    for elem in soup.find_all(text=lambda t: t and "$" in t and any(kw in t.lower() for kw in ["month", "year", "per", "tier", "plan"])):
        text = elem.strip()[:200]
        if text not in pricing:
            pricing.append(text)
    return pricing[:10]


def _extract_features(soup: BeautifulSoup) -> list:
    features = []
    for elem in soup.find_all(["li", "h3", "h4", "strong"]):
        text = elem.get_text(strip=True)
        if 10 < len(text) < 100 and any(kw in text.lower() for kw in ["feature", "benefit", "capability", "include", "support"]):
            if text not in features:
                features.append(text)
    return features[:15]


def _detect_tech_stack(headers: dict, soup: BeautifulSoup) -> list:
    stack = []
    server = headers.get("server", "").lower()
    if "nginx" in server: stack.append("Nginx")
    if "apache" in server: stack.append("Apache")
    
    for script in soup.find_all("script", src=True):
        src = script["src"].lower()
        if "react" in src: stack.append("React")
        if "vue" in src: stack.append("Vue")
        if "next" in src: stack.append("Next.js")
        if "angular" in src: stack.append("Angular")
    
    for link in soup.find_all("link", href=True):
        href = link["href"].lower()
        if "wp-content" in href: stack.append("WordPress")
        if "shopify" in href: stack.append("Shopify")
    
    return list(set(stack))


def _extract_positioning(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)[:200]
    return ""