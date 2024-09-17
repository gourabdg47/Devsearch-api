import aiohttp
from typing import List
from api.models.search_result import SearchResult
from api.config import settings
import logging

logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        self.api_key = settings.SEARCH_API_KEY
        self.custom_search_engine_id = settings.CUSTOM_SEARCH_ENGINE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    async def search(self, query: str, vertical: str, limit: int) -> List[SearchResult]:
        params = {
            "key": self.api_key,
            "cx": self.custom_search_engine_id,
            "q": query,
            "num": limit
        }

        if vertical != "web":
            params["siteSearch"] = self._get_vertical_site(vertical)

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_results(data, vertical)
                else:
                    logger.error(f"Error fetching results from web: {response.status}")
                    return []

    def _get_vertical_site(self, vertical: str) -> str:
        # Define custom vertical sites here
        vertical_sites = {
            "news": "news.google.com",
            "images": "images.google.com",
            "videos": "youtube.com",
            # Add more custom verticals as needed
        }
        return vertical_sites.get(vertical, "")

    def _process_results(self, data: dict, vertical: str) -> List[SearchResult]:
        results = []
        for item in data.get("items", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                vertical=vertical,
                image_url=item.get("pagemap", {}).get("cse_image", [{}])[0].get("src")
            ))
        return results