from fastapi import FastAPI
from routers import mindai_api, query_router  # Import the new router
from config import SERVER_HOST, SERVER_PORT
import uvicorn

app = FastAPI()

# Include routers
app.include_router(mindai_api.router)
app.include_router(query_router.router)  # Register the new router

if __name__ == "__main__":
    print(f"Running bot backend server on http://{SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, reload=True)
