# Marine Data Chatbot Backend

A FastAPI-based backend service for the Marine Data Chatbot that provides intelligent responses about marine science topics including salinity, species, datasets, and oceanographic parameters.

## Features

- **Marine Science Knowledge Base**: Pre-loaded with information about salinity, marine species, oceanographic datasets, temperature, pH, and dissolved oxygen
- **Intelligent Response System**: Analyzes user queries and provides relevant marine data information
- **CORS Enabled**: Configured to work with React frontend applications
- **RESTful API**: Clean and well-documented API endpoints
- **Health Monitoring**: Built-in health check endpoints

## API Endpoints

### POST `/chatbot`
Main chatbot endpoint that processes user messages.

**Request Body:**
```json
{
  "message": "What is ocean salinity?",
  "user_id": "anonymous"
}
```

**Response:**
```json
{
  "response": "Salinity is the measure of dissolved salts in water, typically expressed in parts per thousand (ppt). Ocean water averages about 35 ppt salinity...",
  "status": "success"
}
```

### GET `/`
Health check endpoint.

### GET `/health`
Detailed health check for monitoring.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

1. **Start the development server:**
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **The API will be available at:**
   - Main API: `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Testing the API

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/chatbot" \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about marine species", "user_id": "test_user"}'
```

Or visit `http://localhost:8000/docs` for interactive API documentation.

## Configuration

The server is configured to:
- Run on `0.0.0.0:8000` by default
- Allow CORS requests from common frontend development ports
- Include detailed logging and error handling
- Support hot reloading during development

## Knowledge Base Topics

The chatbot can answer questions about:

- **Salinity**: Salt content, brackish water, freshwater vs saltwater
- **Species**: Marine life, biodiversity, fish, corals, plankton
- **Datasets**: Oceanographic measurements, research data, monitoring
- **Temperature**: Sea surface temperature, thermal effects, climate
- **pH**: Ocean acidification, acidity levels, chemical properties
- **Oxygen**: Dissolved oxygen, hypoxia, marine respiration

## Development

To extend the knowledge base, modify the `MARINE_KNOWLEDGE` dictionary in `main.py`:

```python
MARINE_KNOWLEDGE = {
    "new_topic": {
        "keywords": ["keyword1", "keyword2"],
        "info": "Detailed information about the topic..."
    }
}
```

## Troubleshooting

- **Port already in use**: Change the port in `main.py` or kill the process using port 8000
- **CORS errors**: Ensure your frontend URL is included in the `allow_origins` list
- **Module not found**: Make sure you're in the correct directory and have activated your virtual environment

## Production Deployment

For production deployment, consider:
- Using a production ASGI server like Gunicorn with Uvicorn workers
- Setting up proper environment variables
- Configuring reverse proxy (nginx)
- Implementing proper logging and monitoring
- Adding authentication and rate limiting as needed
