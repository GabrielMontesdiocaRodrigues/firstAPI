from fastapi import FastAPI, Request, Form, Depends, status

from starlette.responses import RedirectResponse
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
def addBook(request: Request, book_title: str = Form('book_title'), book_price: float = Form('book_price'), book_genre: str = 'Undefined', db: Session = Depends(get_db)):
    new_book = models.Book(
        title=book_title, price=book_price, genre=book_genre)
    db.add(new_book)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get('/deleteBook/{book_id}')
def deleteBook(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(book)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get('/updateBook/{book_id}')
def updateBook(request: Request, book_id: int, db: Session = Depends(get_db)):
    updated_book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    updated_book.complete = not updated_book.complete
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
