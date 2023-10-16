from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from time import sleep
from psycopg2.extras import RealDictCursor
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
import psycopg2
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/sqlalchemy")
def test(db: Session = Depends(get_db)):
    return {"status":"success"}
