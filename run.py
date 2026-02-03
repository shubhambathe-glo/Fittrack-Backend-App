"""
Development server runner
For production, use: uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
        log_level="info"
    )
    