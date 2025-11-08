# ProjetAPI - Gestion de Projets Étudiants

Ce projet est une API RESTful développée dans le cadre du module "Versionning et Gestion de Projet". Elle permet de gérer la soumission de projets étudiants pour un cours, en simulant un environnement de développement collaboratif complet, du Git Flow à l'intégration continue (CI/CD) avec GitHub Actions.

## 🎯 Objectifs Pédagogiques

- **Structuration de projet** avec le modèle Git Flow (`main`, `develop`, `feature`).
- **Qualité de code** automatisée via les Git Hooks (`pre-commit`, `black`, `flake8`).
- **Collaboration sur GitHub** (Issues, Pull Requests, Revues de code).
- **Automatisation DevOps** avec les GitHub Actions (CI, tests, notifications).
- **Gestion des secrets** et des configurations d'environnement.

## 🛠️ Stack Technique

- **Backend**: Python 3.11+
- **Framework API**: FastAPI
- **Validation des données**: Pydantic
- **Serveur ASGI**: Uvicorn
- **Qualité de code**: Black (formatage), Flake8 (linting)
- **Hooks Git**: pre-commit

## 🚀 Démarrage Rapide

Suivez ces étapes pour lancer le projet sur votre machine locale.

### 1. Prérequis

- Python 3.10 ou supérieur
- `pip` (le gestionnaire de paquets Python)
- Git

### 2. Installation

1.  **Clonez le dépôt de projet :**
    ```bash
    git clone [URL_DE_VOTRE_DEPOT_GITHUB]
    cd Projet-Api
    ```

2.  **Créez un environnement virtuel :**
    C'est une bonne pratique pour isoler les dépendances du projet.
    ```bash
    python -m venv venv
    ```

3.  **Activez l'environnement virtuel :**
    -   Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    -   Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

4.  **Installez les dépendances :**
    ```bash
    pip install "fastapi[all]"
    pip install fastapi

    uvicorn main:app --reload

    pip install flake8 black

    pip install pre-commit

    pre-commit install

    pip install uvicorn
    ```

5.  **Configurez les Git Hooks (très important !) :**
    Cette commande installe les vérifications automatiques avant chaque commit.
    ```bash
    pre-commit install
    ```

### 3. Lancement du serveur

Une fois l'installation terminée, lancez le serveur de développement :

```bash
uvicorn main:app --reload
```

- `--reload` : Le serveur redémarrera automatiquement après chaque modification du code.

L'API est maintenant accessible !

### 4. Utilisation de l'interface

-   **Interface utilisateur principale** : Ouvrez votre navigateur et allez à [http://127.0.0.1:8000/](http://127.0.0.1:8000/ )
-   **Documentation API (Swagger UI)** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs )
-   **Documentation API alternative (ReDoc)** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc )

## 🗂️ Structure du Projet

```
.
├── .github/workflows/      # Fichiers pour les GitHub Actions (CI, etc.)
├── .gitignore              # Fichiers et dossiers ignorés par Git
├── .pre-commit-config.yaml # Configuration pour les hooks pre-commit
├── db.json                 # Fichier de BDD simulée (ignoré par Git)
├── index.html              # Interface utilisateur simple pour tester l'API
├── main.py                 # Fichier principal de l'application FastAPI
├── README.md               # Ce fichier
└── requirements.txt        # Liste des dépendances Python
```

## Endpoints de l'API

L'API expose les endpoints suivants pour gérer les projets :

| Méthode | Route                               | Description                               |
| :------ | :---------------------------------- | :---------------------------------------- |
| `POST`  | `/projects`                         | Soumettre un nouveau projet.              |
| `GET`   | `/projects`                         | Lister tous les projets soumis.           |
| `GET`   | `/projects/{id}`                    | Obtenir les détails d'un projet.          |
| `PUT`   | `/projects/{id}/grade`              | Assigner une note à un projet.            |
| `DELETE`| `/projects/{id}`                    | Supprimer un projet.                      |
| `GET`   | `/projects/course/{courseName}`     | Filtrer les projets par nom de cours.     |

## 👥 Membres de l'Équipe

-   **[Zidane]** Nom du membre 1 (Lead/Maintainer)
-   **[Ondoa]** Nom du membre 2
-   **[Habiba]** Nom du membre 3
-   **[Chris]** Nom du membre 4
-   **[Ketchemene]** Nom du membre 5
-   **[Gabrielle]** Nom du membre 6
-   **[Rayan]** Nom du membre 7
