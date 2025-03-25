import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "json"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "csv"), exist_ok=True)

    def _generate_filename(self, query: str) -> str:
        """Generate a filename based on the search query and timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Clean the query to make it filesystem-friendly
        clean_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_query = clean_query.replace(' ', '_')
        return f"{clean_query}_{timestamp}"

    def save_results(self, query: str, results: List[Dict[str, Any]]):
        """Save search results in both JSON and CSV formats"""
        filename = self._generate_filename(query)
        
        # Save JSON
        json_path = os.path.join(self.data_dir, "json", f"{filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, f, indent=2, ensure_ascii=False)

        # Save CSV
        csv_path = os.path.join(self.data_dir, "csv", f"{filename}.csv")
        if results:
            # Flatten specifications for CSV
            flattened_results = []
            for result in results:
                flat_result = result.copy()
                specs = flat_result.pop('specifications', [])
                for spec in specs:
                    flat_result[f"spec_{spec['name']}"] = spec['value']
                flattened_results.append(flat_result)

            df = pd.DataFrame(flattened_results)
            df.to_csv(csv_path, index=False, encoding='utf-8')

        return {
            "json_path": json_path,
            "csv_path": csv_path
        }

    def get_recent_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent search results"""
        json_dir = os.path.join(self.data_dir, "json")
        files = sorted(
            [f for f in os.listdir(json_dir) if f.endswith('.json')],
            key=lambda x: os.path.getctime(os.path.join(json_dir, x)),
            reverse=True
        )[:limit]

        recent_searches = []
        for file in files:
            with open(os.path.join(json_dir, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                recent_searches.append({
                    "query": data["query"],
                    "timestamp": data["timestamp"],
                    "result_count": len(data["results"])
                })

        return recent_searches 