# main.py
import json
import uuid  # noqa: F401
from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel
from typing import List  # noqa: F401

# from typing import List

app = FastAPI()

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
    grade: int = None  # Optionnel au début


class ProjectCreate(BaseModel):
    studentName: str
    course: str
    githubUrl: str


class GradeUpdate(BaseModel):
    grade: int
