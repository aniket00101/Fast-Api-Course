from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine
from sqlalchemy.orm import Session


app = FastAPI()

@app.get('/')
def first():
    return {
        'data': 'blogging app'
    }

models.Base.metadata.create_all(bind = engine)


@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return db