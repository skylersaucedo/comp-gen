from anthropic import Anthropic
from typing import List, Dict, Any
import json
from app.core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

class AnthropicService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.max_tokens = settings.MAX_TOKENS

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def search_website(self, website_url: str, asset_description: str) -> List[Dict[str, Any]]:
        prompt = f"""
        You are a construction equipment search assistant. I need you to search for {asset_description} on the following website: {website_url}.

        Please navigate to the site, use appropriate search parameters, and return ALL matching items located in the continental United States.

        For each item found, extract:
        1. Full item description
        2. Exact location
        3. Listed price (if available)
        4. All available specifications
        5. Complete contact information
        6. Current date and time of this search

        Format the results as a JSON array with the following structure for each item:
        {{
            "description": "string",
            "location": "string",
            "price": "string",
            "specifications": [
                {{"name": "string", "value": "string"}}
            ],
            "contact": "string",
            "website": "{website_url}",
            "datetime": "string"
        }}

        Only include items located in the continental United States. Be comprehensive but ensure the total response stays under {self.max_tokens} tokens.
        """

        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=self.max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse the response content as JSON
            results = json.loads(response.content[0].text)
            return results
            
        except Exception as e:
            print(f"Error searching {website_url}: {str(e)}")
            return []

    async def search_all_websites(self, asset_description: str) -> List[Dict[str, Any]]:
        all_results = []
        
        for website in settings.TARGET_WEBSITES:
            results = await self.search_website(website, asset_description)
            all_results.extend(results)
            
        return all_results 