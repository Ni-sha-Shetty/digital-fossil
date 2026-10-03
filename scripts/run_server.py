#!/usr/bin/env python
"""
DIGITAL FOSSIL - Development Server Launcher
"""
import sys
import uvicorn
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

if __name__ == "__main__":
    print("Starting Digital Fossil API Server on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
