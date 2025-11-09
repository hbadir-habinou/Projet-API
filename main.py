# main.py
import json

from fastapi import FastAPI, HTTPException  # noqa: F401
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # noqa: F401
from pydantic import BaseModel
from typing import List, Optional  # noqa: F401

# from typing import List

app = FastAPI(
    title="ProjetAPI Étudiant",
    description="Une API pour gérer les soumissions de projets étudiants.",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


# --- Stockage des données ---
DB_FILE = "db.json"


def read_db():
    """Lit la base de données depuis le fichier JSON."""
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"projects": []}


def write_db(data):
    """Écrit les données dans le fichier JSON."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- Modèles de données (Pydantic) ---
class Project(BaseModel):
    id: str
    studentName: str
    course: str
    githubUrl: str
    grade: Optional[int] = None


class ProjectCreate(BaseModel):
    studentName: str
    course: str
    githubUrl: str


class GradeUpdate(BaseModel):
    grade: int


# Code pour l'Issue #1 : POST /projects
# --- Nouveau endpoint : GET /projects/course/{course_name} ---
# Issue #6: GET /projects/course/{course_name}
@app.get(
    "/projects/course/{course_name}", response_model=List[Project], tags=["Projects"]
)
def get_projects_by_course(course_name: str):
    """Filtrer les projets par nom de cours."""
    db = read_db()
    filtered_projects = [
        p for p in db.get("projects", []) if p["course"].lower() == course_name.lower()
    ]
    return filtered_projects
