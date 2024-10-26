from fastapi import FastAPI
from routers import timetable_router
import uvicorn

app = FastAPI()

app.include_router(timetable_router, prefix="/api/Timetable")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
