from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    asset_description: str = Field(
        ...,
        description="Description of the construction asset to search for",
        example="Carolina Excavation Volvo A40 1500 HPY"
    )
    max_results: Optional[int] = Field(
        default=10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    )

class AssetSpecification(BaseModel):
    name: str
    value: str

class SearchResult(BaseModel):
    description: str = Field(..., description="Full item description")
    location: str = Field(..., description="Location of the asset")
    price: Optional[str] = Field(None, description="Listed price if available")
    specifications: List[AssetSpecification] = Field(default_factory=list)
    contact: Optional[str] = Field(None, description="Contact information")
    website: str = Field(..., description="Source website name")
    datetime: datetime = Field(default_factory=datetime.utcnow)

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResult]
    execution_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow) 