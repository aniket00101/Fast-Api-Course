from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

@app.get('/')
def first():
    return {
        'data': 'blogging app'
    }

models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create blog and store in db
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# delete a particular blog from db using id
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    
    db.commit()
    return {'message': f'Blog {id} deleted successfully'}

#get all blog from db
@app.get('/blog')
def getall(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# get particular blog with id
@app.get('/blog/{id}', status_code= 200)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'details': f'blog with the {id} is not available'}
    return blog

# Update a specific blog by id
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f'Blog with {id} not found')
    blog.update(request.dict())
    db.commit()
    return {'message': 'Updated successfully'}