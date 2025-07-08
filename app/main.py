
from fastapi import FastAPI
import asyncio
from app.database import init_db
from app.scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()
    app.state.account_id = "TU_ACCOUNT_ID"
    app.state.location_id = "TU_LOCATION_ID"
    start_scheduler(app)

@app.get("/")
async def root():
    return {"msg": "Sistema funcionando 🚀"}
