from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from crawler.crawler import Crawler

app = FastAPI(
    title="Product URL Crawler API",
    description="API interface for the web crawler that discovers product URLs from e-commerce sites.",
    version="1.0.0"
)

# Request model for the crawl endpoint.
class CrawlRequest(BaseModel):
    domain: str

# Response model for the crawl endpoint.
class CrawlResponse(BaseModel):
    domain: str
    product_urls: list[str]

@app.post("/crawl", response_model=CrawlResponse)
async def crawl_domain(request: CrawlRequest):
    domain = request.domain
    try:
        crawler = Crawler(domain)
        product_urls = await crawler.run()
        return {"domain": domain, "product_urls": list(product_urls)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

