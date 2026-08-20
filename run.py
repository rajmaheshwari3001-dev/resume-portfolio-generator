import os
import sys

def main():
    try:
        import uvicorn
        import fastapi
    except ImportError:
        print("Error: Required dependencies not found.")
        print("To run the web app locally, please install them first by running:")
        print("pip install fastapi uvicorn")
        sys.exit(1)
        
    print("="*50)
    print("Starting PORTFOLIO.AI Local Web Server...")
    print("="*50)
    print("\nOnce the server starts, open your browser and go to:")
    print(">>> http://localhost:8000 <<<\n")
    print("Press Ctrl+C to stop the server.")
    
    # Run the uvicorn server pointing to the FastAPI app in api/index.py
    uvicorn.run("api.index:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
