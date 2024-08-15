from typing import Optional
from fastapi import FastAPI, Path
from datas import students
from pydantic import BaseModel
from students.schemas import Student
import uvicorn

app = FastAPI()

# Extraction de constante pour les contraintes des IDs d'étudiants
STUDENT_ID_DESCRIPTION = "L'id de l'étudiant que vous recherchez"
STUDENT_ID_CONSTRAINTS = {'ge': 1, 'le': max(students.keys())}


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None


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


@app.put("/students/{student_id}/update")
def update_student(student_id: int, student: UpdateStudent):
    # utiliser model_dump pour une representation dictionnaire de l'objet
    if student_id in students:
        for key, value in student.model_dump().items():
            if value is not None:
                students[student_id][key] = value
        return students[student_id]
    return {"error": f"L'ID {student_id} n'existe pas."}


@app.delete("/students/{student_id}/delete")
def delete_student(student_id: int):
    if student_id in students:
        del students[student_id]
        return {"status": "Deleted successfully"}


def filter_students_by_name(name: str):
    """Filtre les étudiants par nom."""
    return [student for student in students.values() if student['name'] == name]


# Pour le débogage
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
