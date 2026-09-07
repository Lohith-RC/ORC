"""
Oral Cancer Detection System (OSCC AI)
Main Application Entrypoint

This entrypoint imports the modular enterprise application package from app.main.
To run the server:
    python -m uvicorn main:app --host 0.0.0.0 --port 8000
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)