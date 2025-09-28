from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Marine Data Chatbot API",
    description="API for marine data chatbot with salinity, species, and dataset information",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

# Marine data knowledge base
MARINE_KNOWLEDGE = {
    "salinity": {
        "keywords": ["salinity", "salt", "saltwater", "brackish", "freshwater"],
        "info": "Salinity is the measure of dissolved salts in water, typically expressed in parts per thousand (ppt). Ocean water averages about 35 ppt salinity. Salinity affects marine life distribution, water density, and ocean circulation patterns."
    },
    "species": {
        "keywords": ["species", "fish", "marine life", "organisms", "biodiversity", "coral", "plankton"],
        "info": "Marine species include fish, corals, plankton, marine mammals, and countless other organisms. Marine biodiversity is crucial for ecosystem health and provides valuable ecosystem services. Species distribution is influenced by temperature, salinity, depth, and nutrient availability."
    },
    "datasets": {
        "keywords": ["dataset", "data", "measurements", "observations", "research", "monitoring"],
        "info": "Marine datasets include oceanographic measurements, species observations, satellite data, and research findings. Common datasets include temperature, salinity, pH, dissolved oxygen, and species abundance data collected through various monitoring programs."
    },
    "temperature": {
        "keywords": ["temperature", "thermal", "heat", "warming", "climate"],
        "info": "Ocean temperature is a critical parameter affecting marine ecosystems, weather patterns, and climate. Sea surface temperature (SST) is monitored globally via satellites and in-situ measurements. Temperature changes impact species migration, coral bleaching, and ocean circulation."
    },
    "ph": {
        "keywords": ["ph", "acidity", "acidification", "alkaline", "basic"],
        "info": "Ocean pH measures the acidity of seawater. Normal ocean pH is around 8.1. Ocean acidification occurs when CO2 dissolves in seawater, lowering pH and affecting marine organisms, especially those with calcium carbonate shells or skeletons."
    },
    "oxygen": {
        "keywords": ["oxygen", "dissolved oxygen", "hypoxia", "anoxia", "breathing"],
        "info": "Dissolved oxygen is essential for marine life respiration. Oxygen levels vary with depth, temperature, and biological activity. Low oxygen zones (hypoxia) can cause marine life stress or death, often caused by nutrient pollution and climate change."
    }
}

def analyze_message(message: str) -> str:
    """Analyze user message and provide relevant marine data information."""
    message_lower = message.lower()
    
    # Check for specific topics
    for topic, data in MARINE_KNOWLEDGE.items():
        if any(keyword in message_lower for keyword in data["keywords"]):
            return data["info"]
    
    # General marine data responses
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! I'm your marine data assistant. I can help you with information about salinity, marine species, oceanographic datasets, temperature, pH, dissolved oxygen, and other marine science topics. What would you like to know?"
    
    if any(word in message_lower for word in ["help", "what can you do", "capabilities"]):
        return "I can help you with marine data topics including:\n• Salinity and water chemistry\n• Marine species and biodiversity\n• Oceanographic datasets and measurements\n• Temperature and climate data\n• pH and ocean acidification\n• Dissolved oxygen levels\n• General marine science questions\n\nJust ask me about any of these topics!"
    
    if any(word in message_lower for word in ["ocean", "sea", "marine", "water"]):
        return "The ocean is a complex system with many interconnected factors. I can help you understand salinity levels, marine species distribution, oceanographic measurements, and how different parameters like temperature and pH affect marine ecosystems. What specific aspect interests you?"
    
    # Default response for unclear queries
    return "I'm here to help with marine data questions! You can ask me about salinity, marine species, oceanographic datasets, temperature, pH, dissolved oxygen, or any other marine science topic. Could you be more specific about what you'd like to know?"

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Marine Data Chatbot API is running!", "status": "healthy"}

@app.post("/chatbot", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """Main chatbot endpoint that processes user messages."""
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Generate response based on the message
        response_text = analyze_message(request.message.strip())
        
        return ChatResponse(
            response=response_text,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "marine-chatbot-api"}

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
