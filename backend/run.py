#!/usr/bin/env python3
"""
Simple script to run the Marine Data Chatbot API server.
This provides an easy way to start the server with proper configuration.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"🌊 Starting Marine Data Chatbot API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🔧 Debug Mode: {debug}")
    print("Press Ctrl+C to stop the server")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )
