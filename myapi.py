from typing import Optional
from fastapi import FastAPI, Path
from datas import students
from pydantic import BaseModel

app = FastAPI()

# Extraction de constante pour les contraintes des IDs d'étudiants
STUDENT_ID_DESCRIPTION = "L'id de l'étudiant que vous recherchez"
STUDENT_ID_CONSTRAINTS = {'ge': 1, 'le': max(students.keys())}

class Student(BaseModel):
    name: str
    lastname: str
    age: int


@app.get("/")
def fetch_index_data():
    """Retourne un simple dictionnaire de données avec un nom."""
    return {"name": "first data"}


@app.get("/students")
def fetch_all_students():
    """Retourne la liste de tous les étudiants."""
    return students


@app.get("/students/{student_id}")
def fetch_student_by_id(
        student_id: int = Path(description=STUDENT_ID_DESCRIPTION, **STUDENT_ID_CONSTRAINTS), test: Optional[str] = None
):
    """Retourne les données de l'étudiant pour un ID donné."""
    return {
        "students": students[student_id],
        "test": test,
    }


@app.get("/students/name")
def fetch_students_by_name_or_test(
        *, name: Optional[str] = None, test: Optional[int] = None
):
    """
    Retourne une liste d'étudiants filtrée par nom ou une valeur de test si fournie.
    Remarque
    - L'astérisque (*) dans la signature de la fonction force `name` et `test` à être des arguments uniquement nommés,
      ce qui signifie qu'ils doivent être spécifiés par leur mot-clé.
    """
    if name:
        return filter_students_by_name(name)
    elif test is not None:
        return {"data": test}
    return students


@app.post("/students/create")
def create_student(student: Student):
    new_id = max(students.keys()) + 1
    students[new_id] = student
    return students[new_id]


def filter_students_by_name(name: str):
    """Filtre les étudiants par nom."""
    return [student for student in students.values() if student['name'] == name]
