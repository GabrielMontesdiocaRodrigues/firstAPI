from fastapi import FastAPI, Request, Form, Depends

from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
from dataBase import SessionLocal, engine

import models

models.Base.metadata.create_all(bind=engine)

template = Jinja2Templates("template")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home(request: Request, db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return template.TemplateResponse('index.html', {'request': request, 'books_list': books})


@app.post('/addBook')
def addBook():
    pass
