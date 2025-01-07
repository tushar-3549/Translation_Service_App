import openai
from sqlalchemy.orm import Session
from app.crud import update_translation_task 
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def perform_translation(task: int, text: str, languages: list, db: Session):
    translations = {} 
    for lang in languages:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that translates text."
                    },
                    {
                        "role": "user",
                        "content": f"Translate the following text to {lang}: {text}"
                    },
                ],
            )
            translation = response['choices'][0]['message']['content'].strip()
            translations[lang] = translation
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = None  

    update_translation_task(db, task_id=task, translations=translations)
    return translations
