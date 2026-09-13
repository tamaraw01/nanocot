#!/usr/bin/env python3
"""NanoCoT Startup & Deployment Script"""

import sys
import os

def check_requirements():
    """Verify dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import httpx
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env():
    """Verify environment variables are set."""
    if not os.getenv("UPSTREAM_BASE_URL"):
        print("⚠️  UPSTREAM_BASE_URL not set. Using default: http://localhost:20128/v1")
    if not os.getenv("UPSTREAM_API_KEY"):
        print("⚠️  UPSTREAM_API_KEY not set. Using default: sk-dummy")

def main():
    print("🚀 NanoCoT Proxy Engine v1.0.0")
    print("-" * 40)
    
    if not check_requirements():
        sys.exit(1)
    
    check_env()
    
    print("\n✓ Checks passed.")
    print("Starting proxy on http://0.0.0.0:8888")
    print("Press Ctrl+C to stop.\n")
    
    from server import app
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")

if __name__ == "__main__":
    main()
