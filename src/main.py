from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.api.auth import router as router_users
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities

app = FastAPI()

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
