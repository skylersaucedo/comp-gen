from fastapi import APIRouter, HTTPException, Depends
from app.models.search import SearchRequest, SearchResponse, SearchResult
from app.services.anthropic import AnthropicService
from app.services.storage import StorageService
import time
from typing import List

router = APIRouter()
anthropic_service = AnthropicService()
storage_service = StorageService()

@router.post("/search", response_model=SearchResponse)
async def search_assets(request: SearchRequest):
    """
    Search for construction assets across multiple industry websites.
    
    This endpoint uses Anthropic's MCP to search through various construction equipment websites
    and return structured data about matching assets located in the continental United States.
    """
    try:
        start_time = time.time()
        
        # Perform search across all websites
        results = await anthropic_service.search_all_websites(request.asset_description)
        
        # Limit results if specified
        if request.max_results:
            results = results[:request.max_results]
        
        # Save results to storage
        storage_paths = storage_service.save_results(request.asset_description, results)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        return SearchResponse(
            query=request.asset_description,
            total_results=len(results),
            results=results,
            execution_time=execution_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while searching for assets: {str(e)}"
        )

@router.get("/recent-searches")
async def get_recent_searches(limit: int = 10):
    """
    Retrieve information about recent searches performed through the API.
    """
    try:
        return storage_service.get_recent_searches(limit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving recent searches: {str(e)}"
        ) 