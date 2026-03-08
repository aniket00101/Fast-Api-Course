from fastapi import FastAPI
from typing import Optional
import uvicorn 
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def index ():
    return {"name" : "Aniket"}

# Query Parameter
@app.get('/blog')
def blog(limit = 10, published : bool = True, sort: Optional[str] = None):
    if(published):
         return {'data' : f'{limit} blog list from database'}
    else:
        return {'data': 'Return 10 blog from the database'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'All unpublished blog'}

@app.get('/blog/{id}')
def blog(id:  int):
    return {
        "data" : {
            "name" : id
        }
    }

@app.get('/blog/{id}/comments')
def comment(id, limit = 10):
    return {
        'data': {'1', '2'}
    }

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'Blog is created title {blog.title}'}

