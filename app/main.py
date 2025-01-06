from fastapi import FastAPI, status, Depends, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app import schemas
from app import crud

app = FastAPI()
templetes = Jinja2Templates(directory="app/templates")
@app.get('/')
def home():
    return {"message": "welcome to api integration project"}
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
def translate(request: schemas.TranslationRequest):
    pass # next start from here