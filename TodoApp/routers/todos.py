from fastapi import Depends, HTTPException, Path, APIRouter
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine, sessionLocal
from starlette import status

routers = APIRouter()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=5, max_length=100)
    priority : int = Field(gt=0, lt=5)
    complete : bool = Field()

@routers.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@routers.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

"""
New to learn. Validation
from starlette import status = @app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
Path = async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
"""

@routers.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todos(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    print(todo_model)
    db.add(todo_model)
    db.commit()


@routers.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,  todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@routers.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Not Found.")
    db.delete(todo_model)
    db.commit()