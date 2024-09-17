import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.search_engine import SearchEngine
from api.config import settings

async def populate_elasticsearch():
    search_engine = SearchEngine()
    
    # Sample data
    documents = [
        {
            "title": "12 Rules for Life",
            "url": "https://example.com/12-rules-for-life",
            "content": "An Antidote to Chaos is a 2018 self-help book by Canadian clinical psychologist and psychology professor Jordan Peterson...",
            "vertical": "web"
        },
        
    ]

    await search_engine.bulk_index("web_index", documents)
    print("Indexed sample documents")

    await search_engine.close()

if __name__ == "__main__":
    asyncio.run(populate_elasticsearch())