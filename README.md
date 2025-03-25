# Construction Asset Search API

A FastAPI-based service that uses Anthropic's Multimodal Claude Platform (MCP) to search for construction assets across multiple industry websites. The service provides structured data about matching assets located in the continental United States.

## Features

- Search across multiple construction equipment websites
- Structured data extraction using Anthropic MCP
- Results filtering to continental United States
- JSON and CSV export of search results
- Docker containerization for easy deployment
- Rate limiting and efficient token usage
- Comprehensive API documentation
- Automated test suite

## Target Websites

1. ForestryTrader.com
2. RB Auction
3. RitchieSpecs
4. Lectura Specs
5. IronPlanet
6. Forklift Inventory
7. Machinery Trader

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Anthropic API key
- Jupyter Notebook (for interactive testing)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd construction-asset-search
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment variables file and update with your settings:
```bash
cp .env.example .env
# Edit .env with your Anthropic API key and other settings
```

## Running the Application

### Using Docker (Recommended)

1. Build and start the container:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

### Running Locally

1. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at `http://localhost:8000`

## Testing

The project includes two testing approaches:

### 1. Automated Test Script

Run the automated test suite using the Python script:
```bash
python test.py
```

This will execute all test cases in sequence:
- Root endpoint test
- Search endpoint test
- Recent searches test
- Error handling test
- Rate limiting test

### 2. Interactive Testing with Jupyter Notebook

For interactive testing and development, use the provided Jupyter notebook:
```bash
jupyter notebook test.ipynb
```

The notebook includes the following test cases:

#### Test 1: Root Endpoint
```python
response = requests.get(f"{BASE_URL}/")
print("Status Code:", response.status_code)
print("Response:", response.json())
```

#### Test 2: Search Endpoint
```python
search_payload = {
    "asset_description": "Carolina Excavation Volvo A40 1500 HPY",
    "max_results": 5
}
response = requests.post(f"{BASE_URL}/api/search", json=search_payload)
```

#### Test 3: Recent Searches
```python
response = requests.get(f"{BASE_URL}/api/recent-searches", params={"limit": 5})
```

#### Test 4: Error Handling
```python
invalid_payload = {"max_results": 5}
response = requests.post(f"{BASE_URL}/api/search", json=invalid_payload)
```

#### Test 5: Rate Limiting
```python
for i in range(3):
    response = requests.post(
        f"{BASE_URL}/api/search",
        json={"asset_description": f"Test request {i+1}", "max_results": 1}
    )
    time.sleep(1)
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Endpoints

#### POST /api/search
Search for construction assets across multiple websites.

Request body:
```json
{
    "asset_description": "Carolina Excavation Volvo A40 1500 HPY",
    "max_results": 10
}
```

Response:
```json
{
    "query": "Carolina Excavation Volvo A40 1500 HPY",
    "total_results": 5,
    "results": [
        {
            "description": "string",
            "location": "string",
            "price": "string",
            "specifications": [
                {
                    "name": "string",
                    "value": "string"
                }
            ],
            "contact": "string",
            "website": "string",
            "datetime": "string"
        }
    ],
    "execution_time": 0.0,
    "timestamp": "string"
}
```

#### GET /api/recent-searches
Retrieve information about recent searches.

Query parameters:
- `limit`: Maximum number of recent searches to return (default: 10)

## AWS EC2 Deployment

1. Launch an EC2 instance with Ubuntu Server 22.04 LTS
2. SSH into your instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. Install Docker and Docker Compose:
```bash
# Update system
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Clone the repository and set up the application:
```bash
git clone <repository-url>
cd construction-asset-search
cp .env.example .env
# Edit .env with your settings
```

5. Build and start the container:
```bash
docker-compose up -d --build
```

6. Configure security group to allow inbound traffic on port 8000

7. Access the API at `http://your-instance-ip:8000`

## Data Storage

Search results are stored in:
- JSON format: `data/json/`
- CSV format: `data/csv/`

Files are named using the pattern: `{query}_{timestamp}.{extension}`

## Monitoring and Logging

- Application logs are stored in the `logs/` directory
- Docker container logs can be viewed using:
```bash
docker-compose logs -f
```

## Security Considerations

1. API Key Management
   - Store the Anthropic API key in environment variables
   - Never commit API keys to version control
   - Use AWS Secrets Manager or similar for production

2. Rate Limiting
   - The API implements rate limiting to prevent abuse
   - Configure limits in the `.env` file

3. Input Validation
   - All inputs are validated using Pydantic models
   - SQL injection and XSS protection are implemented

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 