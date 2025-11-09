# main.py
import json
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # noqa: F401
from pydantic import BaseModel
from typing import List, Optional  # noqa: F401

app = FastAPI(
    title="ProjetAPI Étudiant",
    description="Une API pour gérer les soumissions de projets étudiants.",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
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
@app.post("/projects", tags=["Projects"])
def create_project(project_data: ProjectCreate):
    """Soumettre un nouveau projet."""
    try:
        db = read_db()
        new_project = Project(id=str(uuid.uuid4()), **project_data.dict())
        db["projects"].append(new_project.dict())
        write_db(db)
        return {
            "success": True,
            "message": "Projet créé avec succès",
            "data": new_project.dict()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors de la création du projet", "error": str(e)}
        )


# Issue #4: PUT /projects/{project_id}/grade
@app.put("/projects/{project_id}/grade", tags=["Projects"])
def grade_project(project_id: str, grade_update: GradeUpdate):
    """Permettre à un 'professeur' de noter un projet."""
    try:
        db = read_db()
        project_to_update = None
        for project in db.get("projects", []):
            if project["id"] == project_id:
                project["grade"] = grade_update.grade
                project_to_update = project
                break
        if not project_to_update:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": f"Projet avec l'ID '{project_id}' introuvable"}
            )
        write_db(db)
        return {
            "success": True,
            "message": "Note attribuée avec succès",
            "data": project_to_update
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors de l'attribution de la note", "error": str(e)}
        )


# Issue #2: GET /projects
@app.get("/projects", tags=["Projects"])
def get_all_projects():
    """Lister tous les projets soumis."""
    try:
        db = read_db()
        projects = db.get("projects", [])
        return {
            "success": True,
            "message": f"{len(projects)} projet(s) récupéré(s) avec succès",
            "data": projects
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors de la récupération des projets", "error": str(e)}
        )


# Issue #5: DELETE /projects/{project_id}
@app.delete("/projects/{project_id}", tags=["Projects"])
def delete_project(project_id: str):
    """Supprimer une soumission de projet."""
    try:
        db = read_db()
        initial_count = len(db.get("projects", []))
        db["projects"] = [p for p in db["projects"] if p["id"] != project_id]
        if len(db["projects"]) == initial_count:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": f"Projet avec l'ID '{project_id}' introuvable"}
            )
        write_db(db)
        return {
            "success": True,
            "message": f"Projet avec l'ID '{project_id}' supprimé avec succès"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors de la suppression du projet", "error": str(e)}
        )


# Issue #6: GET /projects/course/{course_name}
@app.get("/projects/course/{course_name}", tags=["Projects"])
def get_projects_by_course(course_name: str):
    """Filtrer les projets par nom de cours."""
    try:
        db = read_db()
        filtered_projects = [
            p for p in db.get("projects", []) if p["course"].lower() == course_name.lower()
        ]
        return {
            "success": True,
            "message": f"{len(filtered_projects)} projet(s) trouvé(s) pour le cours '{course_name}'",
            "data": filtered_projects
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors du filtrage des projets", "error": str(e)}
        )


# Issue #3: GET /projects/{project_id}
@app.get("/projects/{project_id}", tags=["Projects"])
def get_project_by_id(project_id: str):
    """Obtenir les détails d'un projet par son ID."""
    try:
        db = read_db()
        for project in db.get("projects", []):
            if project["id"] == project_id:
                return {
                    "success": True,
                    "message": "Projet récupéré avec succès",
                    "data": project
                }
        raise HTTPException(
            status_code=404,
            detail={"success": False, "message": f"Projet avec l'ID '{project_id}' introuvable"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Erreur lors de la récupération du projet", "error": str(e)}
        )