"""
Backend Application Entry Point.

Runs the local development server or serves as WSGI entry.
"""

import os
from app import create_app

# Instantiate application using environment config
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    
    print(f"\n=======================================================")
    print(f"[*] SMART RECRUITMENT & PLACEMENT API SERVER")
    print(f"[*] Running at: http://{host}:{port}/api/health")
    print(f"[*] Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"=======================================================\n")
    
    app.run(host=host, port=port, debug=debug)
