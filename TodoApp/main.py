from fastapi import FastAPI, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine, sessionLocal
from starlette import status
from routers import auth, todos

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(auth.routers)
app.include_router(todos.routers)

