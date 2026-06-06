#!/usr/bin/env python
"""Entry point for the backend application"""
import os
from app.main import app

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        debug=os.getenv("ENVIRONMENT") == "development",
        use_reloader=False  # Disable auto-reload to prevent database issues
    )
