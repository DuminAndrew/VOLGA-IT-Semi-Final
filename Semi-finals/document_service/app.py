from fastapi import FastAPI
from routers import document_router
import uvicorn

app = FastAPI()

app.include_router(document_router, prefix="/api/History")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8084)
