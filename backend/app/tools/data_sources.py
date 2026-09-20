from typing import Dict, Any, Optional
import asyncio
import httpx
from app.core.config import settings


class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
    
    async def get_sector_performance(self) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.BASE_URL, params={
                "function": "SECTOR",
                "apikey": self.api_key
            })
            return resp.json() if resp.status_code == 200 else {}
    
    async def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.BASE_URL, params={
                "function": "OVERVIEW",
                "symbol": symbol,
                "apikey": self.api_key
            })
            return resp.json() if resp.status_code == 200 else {}
    
    async def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(self.BASE_URL, params={
                "function": "INCOME_STATEMENT",
                "symbol": symbol,
                "apikey": self.api_key
            })
            return resp.json() if resp.status_code == 200 else {}


class FinnhubClient:
    BASE_URL = "https://finnhub.io/api/v1"
    
    def __init__(self):
        self.api_key = settings.FINNHUB_API_KEY
    
    async def get_company_news(self, symbol: str, from_date: str, to_date: str) -> list:
        if not self.api_key:
            return []
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self.BASE_URL}/company-news", params={
                "symbol": symbol,
                "from": from_date,
                "to": to_date,
                "token": self.api_key
            })
            return resp.json() if resp.status_code == 200 else []
    
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self.BASE_URL}/quote", params={
                "symbol": symbol,
                "token": self.api_key
            })
            return resp.json() if resp.status_code == 200 else {}
    
    async def get_news_sentiment(self) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self.BASE_URL}/news-sentiment", params={
                "token": self.api_key
            })
            return resp.json() if resp.status_code == 200 else {}


class FREDClient:
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    def __init__(self):
        self.api_key = settings.FRED_API_KEY
    
    async def get_series(self, series_id: str, limit: int = 1) -> Dict[str, Any]:
        if not self.api_key:
            return {}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{self.BASE_URL}/series/observations", params={
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "limit": limit,
                "sort_order": "desc"
            })
            return resp.json() if resp.status_code == 200 else {}
    
    async def get_macro_indicators(self) -> Dict[str, float]:
        series_map = {
            "gdp_growth": "A191RL1Q225SBEA",
            "inflation_rate": "CPIAUCSL",
            "fed_funds_rate": "FEDFUNDS",
            "unemployment_rate": "UNRATE",
            "consumer_confidence": "UMCSENT",
            "retail_sales": "RSAFS",
            "industrial_production": "INDPRO",
        }
        
        result = {}
        for name, series_id in series_map.items():
            data = await self.get_series(series_id)
            observations = data.get("observations", [])
            if observations:
                try:
                    result[name] = float(observations[0]["value"])
                except (ValueError, KeyError):
                    pass
        return result


class YFinanceClient:
    def __init__(self):
        pass
    
    async def get_ticker_info(self, symbol: str) -> Dict[str, Any]:
        def _sync():
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            return ticker.info
        try:
            return await asyncio.to_thread(_sync)
        except Exception:
            return {}
    
    async def get_historical_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        def _sync():
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist.to_dict() if not hist.empty else {}
        try:
            return await asyncio.to_thread(_sync)
        except Exception:
            return {}
    
    async def get_sector_etf_performance(self) -> Dict[str, Any]:
        sector_etfs = {
            "technology": "XLK",
            "healthcare": "XLV",
            "financials": "XLF",
            "consumer_discretionary": "XLY",
            "consumer_staples": "XLP",
            "energy": "XLE",
            "industrials": "XLI",
            "materials": "XLB",
            "real_estate": "XLRE",
            "utilities": "XLU",
            "communication_services": "XLC",
        }
        
        result = {}
        for sector, etf in sector_etfs.items():
            data = await self.get_historical_data(etf, "1y")
            if data and "Close" in data:
                closes = list(data["Close"].values())
                if len(closes) >= 2:
                    result[sector] = {
                        "current": closes[-1],
                        "yoy_change": (closes[-1] - closes[0]) / closes[0] if closes[0] else 0
                    }
        return result


class ApifyClient:
    BASE_URL = "https://api.apify.com/v2"
    
    def __init__(self):
        self.token = settings.APIFY_API_TOKEN
    
    async def run_actor(self, actor_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.token:
            return {}
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{self.BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items",
                params={"token": self.token},
                json=input_data
            )
            return resp.json() if resp.status_code == 200 else {}
    
    async def scrape_website(self, url: str) -> Dict[str, Any]:
        return await self.run_actor("apify/website-content-crawler", {
            "startUrls": [{"url": url}],
            "maxPagesPerCrawl": 10,
            "removeCookieWarnings": True,
        })


class PyTrendsClient:
    def __init__(self):
        pass
    
    async def get_interest_over_time(self, keywords: list, timeframe: str = "today 12-m") -> Dict[str, Any]:
        def _sync():
            from pytrends.request import TrendReq
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload(keywords, timeframe=timeframe)
            df = pytrends.interest_over_time()
            return df.to_dict() if not df.empty else {}
        try:
            return await asyncio.to_thread(_sync)
        except Exception:
            return {}
    
    async def get_related_queries(self, keyword: str) -> Dict[str, Any]:
        def _sync():
            from pytrends.request import TrendReq
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload([keyword])
            return pytrends.related_queries()
        try:
            return await asyncio.to_thread(_sync)
        except Exception:
            return {}