import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# --- Création de l'application ---
app = FastAPI(
    title="ProjetAPI Étudiant",
    description="Une API pour gérer les soumissions de projets étudiants.",
    version="1.0.0",
)

# === CORSMiddleware pour autoriser ton front-end ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # tu peux remplacer "*" par ["http://localhost:8000"] si tu veux restreindre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes principales ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)


# --- Gestion de la "base de données" JSON ---
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


# --- Modèles Pydantic ---
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


# --- Endpoints de l'API ---
@app.post("/projects", response_model=Project)
def create_project(project_data: ProjectCreate):
    """Soumettre un nouveau projet."""
    db = read_db()
    new_project = Project(id=str(uuid.uuid4()), **project_data.dict())
    db["projects"].append(new_project.dict())
    write_db(db)
    return new_project


@app.get("/projects", response_model=List[Project])
def get_all_projects():
    """Lister tous les projets soumis."""
    db = read_db()
    return db.get("projects", [])


@app.get("/projects/{project_id}", response_model=Project)
def get_project_by_id(project_id: str):
    """Obtenir les détails d'un projet par son ID."""
    db = read_db()
    for project in db.get("projects", []):
        if project["id"] == project_id:
            return project
    raise HTTPException(
        status_code=404, detail=f"Project with ID '{project_id}' not found"
    )


@app.get("/projects/course/{course_name}", response_model=List[Project])
def get_projects_by_course(course_name: str):
    """Filtrer les projets par nom de cours."""
    db = read_db()
    filtered = [
        p for p in db.get("projects", []) if p["course"].lower() == course_name.lower()
    ]
    return filtered


@app.put("/projects/{project_id}/grade", response_model=Project)
def grade_project(project_id: str, grade_update: GradeUpdate):
    """Attribuer une note à un projet."""
    db = read_db()
    for project in db.get("projects", []):
        if project["id"] == project_id:
            project["grade"] = grade_update.grade
            write_db(db)
            return project
    raise HTTPException(
        status_code=404, detail=f"Project with ID '{project_id}' not found"
    )


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str):
    """Supprimer un projet."""
    db = read_db()
    initial_count = len(db.get("projects", []))
    db["projects"] = [p for p in db["projects"] if p["id"] != project_id]
    if len(db["projects"]) == initial_count:
        raise HTTPException(
            status_code=404, detail=f"Project with ID '{project_id}' not found"
        )
    write_db(db)
    return


@app.put("/projects/{project_id}")
def update_project(project_id: str, updated_data: dict):
    """Met à jour un projet existant (nom, cours, githubUrl)."""
    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Trouver le projet correspondant
    for project in data["projects"]:
        if project["id"] == project_id:
            project["studentName"] = updated_data.get(
                "studentName", project["studentName"]
            )
            project["course"] = updated_data.get("course", project["course"])
            project["githubUrl"] = updated_data.get("githubUrl", project["githubUrl"])

            with open("db.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return {"message": "Projet mis à jour avec succès", "project": project}

    raise HTTPException(status_code=404, detail="Projet non trouvé")
