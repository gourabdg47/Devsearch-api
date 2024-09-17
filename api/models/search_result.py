from pydantic import BaseModel, HttpUrl
from typing import Optional

class SearchResult(BaseModel):
    title: str
    url: HttpUrl
    snippet: str
    vertical: str
    image_url: Optional[HttpUrl] = None
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Example Search Result",
                "url": "https://example.com",
                "snippet": "This is a brief description of the search result...",
                "vertical": "web",
                "image_url": "https://example.com/image.jpg"
            }
        }
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": str(self.url),
            "snippet": self.snippet,
            "vertical": self.vertical,
            "image_url": str(self.image_url) if self.image_url else None
        }