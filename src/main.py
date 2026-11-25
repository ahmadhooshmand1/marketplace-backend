from fastapi import Depends, FastAPI
from psycopg import Connection

from src.api.user import router as user_router
from src.connections.db import get_db

app = FastAPI(title="marketplace Backend API")

app.include_router(user_router)


@app.get("/health")
def health_check(db: Connection = Depends(get_db)):
    result = db.execute("SELECT current_database()").fetchone()
    return {
        "status": "ok",
        "database": result["current_database"],
    }