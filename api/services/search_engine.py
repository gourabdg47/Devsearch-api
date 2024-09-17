from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk
from api.models.search_result import SearchResult
from api.config import settings
from api.services.web_search import WebSearch
import logging
from typing import List

logger = logging.getLogger(__name__)

class SearchEngine:
    def __init__(self):
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        self.web_search = WebSearch()

    async def ensure_index(self, index_name: str):
        try:
            if not await self.es.indices.exists(index=index_name):
                await self.es.indices.create(index=index_name)
                logger.info(f"Created index: {index_name}")
        except Exception as e:
            logger.error(f"Error ensuring index {index_name}: {str(e)}")
            raise

    async def search(self, query: str, vertical: str, limit: int) -> List[SearchResult]:
        index = f"{vertical}_index"
        try:
            await self.ensure_index(index)
            resp = await self.es.search(
                index=index,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "content"]
                        }
                    },
                    "size": limit
                }
            )
            results = self._process_elasticsearch_results(resp, vertical)
            
            if not results:
                # Fallback to web search if no local results
                results = await self.web_search.search(query, vertical, limit)
                
                # Index the web results for future use
                await self.bulk_index(index, [result.to_dict() for result in results])
            
            return results
        except NotFoundError:
            logger.error(f"Index not found: {index}")
            return await self.web_search.search(query, vertical, limit)
        except Exception as e:
            logger.error(f"Error searching in vertical '{vertical}': {str(e)}")
            raise ValueError(f"Error searching in vertical '{vertical}': {str(e)}")

    def _process_elasticsearch_results(self, resp, vertical) -> List[SearchResult]:
        results = []
        for hit in resp['hits']['hits']:
            results.append(SearchResult(
                title=hit['_source'].get('title', ''),
                url=hit['_source'].get('url', ''),
                snippet=hit['_source'].get('content', '')[:200] + "...",
                vertical=vertical,
                image_url=hit['_source'].get('image_url')
            ))
        return results

    async def index_document(self, index: str, doc: dict):
        await self.ensure_index(index)
        await self.es.index(index=index, body=doc)

    async def bulk_index(self, index: str, documents: List[dict]):
        await self.ensure_index(index)
        actions = [
            {
                "_index": index,
                "_source": doc
            }
            for doc in documents
        ]
        await async_bulk(self.es, actions)

    async def close(self):
        await self.es.close()