# Construction Asset Search API with Anthropic MCP

## Project Overview
Create a FastAPI backend service (Docker-ready) that uses Anthropic's Multimodal Claude Platform (MCP) to search for construction assets across multiple industry websites. The service should handle search requests containing asset descriptions, search through specified websites, and return structured data about matching assets found in the continental United States.

## Core Requirements

### API Framework
- Build using FastAPI for high performance and easy documentation
- Implement Docker containerization for easy deployment
- Design with rate limiting and efficient token usage in mind for Anthropic API

### Target Websites to Search
1. https://www.forestrytrader.com/listings/search?sort=1
2. https://www.rbauction.com/
3. https://www.ritchiespecs.com
4. https://www.lectura-specs.com/en/specs/forklifts/diesel-forklifts
5. https://www.ironplanet.com/ (focus on "Browse by category")
6. https://www.forkliftinventory.com/
7. https://www.machinerytrader.com/listings/for-sale/forklifts/1036
   - Include "By Category" searches
   - Include "By Power Type" searches (at bottom of page)

### Request/Response Structure
- **Input**: Asset description text (e.g., "Carolina Excavation Volvo A40 1500 HPY")
- **Output**: JSON array of search results with structured data

### Data Requirements
For each matching asset found, capture:
- Item description
- Location (filter to continental United States only)
- Price
- Specifications
- Contact information
- Website name (source)
- Datetime of viewing

### Storage Requirements
- Save results in both JSON and CSV formats
- Create structured file naming system based on search queries
- Store files in project directory with appropriate organization

### Anthropic MCP Integration
- Implement efficient token management (max 8,000 tokens per request)
- Handle rate limiting with appropriate backoff strategies
- Design system to minimize token usage while maximizing search coverage

## Technical Implementation Details

### Project Structure
```
construction-asset-search/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── search.py    # Search endpoint implementation
│   ├── core/                # Core application code
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration settings
│   │   └── logging.py       # Logging configuration
│   ├── services/            # Service layer
│   │   ├── __init__.py
│   │   ├── anthropic.py     # Anthropic MCP client
│   │   ├── search_engine.py # Search orchestration
│   │   └── storage.py       # Results storage (JSON/CSV)
│   └── models/              # Data models
│       ├── __init__.py
│       └── search.py        # Search request/response models
├── data/                    # Directory for storing results
├── logs/                    # Application logs
├── tests/                   # Test suite
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker compose configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md                # Project documentation
```

### Key Components to Implement

#### 1. FastAPI Application
- Create main.py with FastAPI app initialization
- Implement proper error handling and logging
- Include Swagger documentation with example requests/responses

#### 2. Search Endpoint
- Implement POST endpoint at `/api/search`
- Accept JSON body with asset description
- Return structured search results
- Include appropriate validation and error handling

#### 3. Anthropic MCP Service
- Create service to interact with Anthropic's API
- Implement efficient prompting strategy to maximize search effectiveness
- Handle token limits and rate limiting
- Process and extract structured data from responses

#### 4. Search Engine Orchestration
- Create a service to manage searching across multiple websites
- Implement parallel processing where appropriate
- Handle website-specific search patterns
- Filter results to continental US locations

#### 5. Storage Service
- Implement JSON and CSV export functionality
- Create consistent naming and organization scheme
- Handle file system operations safely

#### 6. Data Models
- Define Pydantic models for requests and responses
- Implement validation logic for all data fields
- Create consistent structure for search results

#### 7. Docker Configuration
- Create Dockerfile optimized for Python/FastAPI
- Include appropriate base image, dependencies, and configuration
- Configure for production deployment

## Implementation Strategy

### Anthropic MCP Integration
For each website:

1. First, have Claude navigate to the website and understand its search structure
2. Formulate appropriate search queries based on asset description
3. Extract relevant listing information from search results
4. Structure the data according to our required format
5. Handle pagination and result limits appropriately

Example prompt structure for Anthropic:
```python
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
  "specifications": "string",
  "contact": "string",
  "website": "{website_name}",
  "datetime": "string"
}}

Only include items located in the continental United States. Be comprehensive but ensure the total response stays under 8000 tokens.
"""
```

### AWS EC2 Deployment Instructions
Include detailed instructions in the README for:
1. Setting up an EC2 instance
2. Installing Docker and Docker Compose
3. Configuring environment variables
4. Running the application
5. Setting up monitoring and logging
6. Managing API keys securely

## Additional Requirements

### Error Handling & Resilience
- Implement robust error handling for API failures
- Add retry mechanisms with exponential backoff
- Log all errors with appropriate detail
- Create fallback strategies for partial search failures

### Performance Optimization
- Implement caching where appropriate
- Use async/await for concurrent requests
- Optimize token usage in Anthropic prompts
- Consider batching requests when possible

### Security Considerations
- Secure API key management
- Input validation and sanitization
- Rate limiting for API endpoints
- Proper logging (without sensitive data)

## Deliverables
1. Complete FastAPI application with all functionality
2. Docker configuration for easy deployment
3. Comprehensive README with:
   - API documentation
   - Request/response examples
   - Deployment instructions for AWS EC2
   - Configuration options
4. Requirements.txt file with all dependencies
5. Example search results in both JSON and CSV formats
