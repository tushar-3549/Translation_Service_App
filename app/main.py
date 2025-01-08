
from fastapi import FastAPI, status, Depends, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app import schemas, crud, models
from app.utils import perform_translation
from app.database import get_db, engine, SessionLocal
from typing import List
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templetes = Jinja2Templates(directory="app/templates")

@app.get('/')
def home():
    return {"message": "Welcome to the API integration project"}

@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templetes.TemplateResponse("index.html", {"request": request})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.post('/translate', response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        task = crud.create_translation_task(db, request.text, request.languages)
        background_tasks.add_task(perform_translation, task.id, request.text, request.languages, db)
        return {"task_id": task.id}  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Translation failed: {str(e)}")


@app.get('/translate/{task_id}', response_model=schemas.TranslationStatus)
def get_translate(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task.id, "status": task.status, "translations": task.translation}  

@app.get("/translate/content/{task_id}", response_model=schemas.TranslationStatus)
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task
