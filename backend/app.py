from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

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

def analyze_message(message):
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

@app.route('/')
def root():
    """Health check endpoint."""
    return jsonify({
        "message": "Marine Data Chatbot API is running!", 
        "status": "healthy"
    })

@app.route('/chatbot', methods=['POST'])
def chat_with_bot():
    """Main chatbot endpoint that processes user messages."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required"
            }), 400
        
        message = data['message']
        user_id = data.get('user_id', 'anonymous')
        
        if not message or not message.strip():
            return jsonify({
                "error": "Message cannot be empty"
            }), 400
        
        # Generate response based on the message
        response_text = analyze_message(message.strip())
        
        return jsonify({
            "response": response_text,
            "status": "success"
        })
    
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy", 
        "service": "marine-chatbot-api"
    })

if __name__ == '__main__':
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"🌊 Starting Marine Data Chatbot API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print("Press Ctrl+C to stop the server")
    
    # Run the server
    app.run(host=host, port=port, debug=debug)
