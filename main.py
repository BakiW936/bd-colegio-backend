from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Result
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def query(sql: str):
    with engine.connect() as conn:
        result: Result = conn.execute(sql)
        return [dict(row._mapping) for row in result]

@app.get("/")
def root():
    return {"message": "API colegio funcionando", "status": "OK"}

# 1) Profesores que NO dictan clases
@app.get("/profesores-sin-clases")
def profesores_sin_clases():
    sql = """
    SELECT p.id, p.nombre
    FROM profesor p
    LEFT JOIN curso c ON p.id = c.profesor_id
    WHERE c.id IS NULL;
    """
    return query(sql)

# 2) Profesores que dictan MÁS de una clase
@app.get("/profesores-mas-de-una-clase")
def profesores_mas_de_una_clase():
    sql = """
    SELECT p.id, p.nombre, COUNT(c.id) AS total_clases
    FROM profesor p
    JOIN curso c ON p.id = c.profesor_id
    GROUP BY p.id, p.nombre
    HAVING COUNT(c.id) > 1;
    """
    return query(sql)

# 3) Profesores que dictan SOLO una clase
@app.get("/profesores-solo-una-clase")
def profesores_solo_una_clase():
    sql = """
    SELECT p.id, p.nombre, COUNT(c.id) AS total_clases
    FROM profesor p
    JOIN curso c ON p.id = c.profesor_id
    GROUP BY p.id, p.nombre
    HAVING COUNT(c.id) = 1;
    """
    return query(sql)

# 4) Cursos con MÁS de 2 estudiantes inscritos
@app.get("/cursos-mas-de-dos-estudiantes")
def cursos_mas_de_dos_estudiantes():
    sql = """
    SELECT c.id, c.nombre, COUNT(m.estudiante_id) AS total_estudiantes
    FROM curso c
    JOIN matricula m ON c.id = m.curso_id
    GROUP BY c.id, c.nombre
    HAVING COUNT(m.estudiante_id) > 2;
    """
    return query(sql)

# 5) Estudiantes NO matriculados en ningún curso
@app.get("/estudiantes-sin-matriculas")
def estudiantes_sin_matriculas():
    sql = """
    SELECT e.id, e.nombre
    FROM estudiante e
    LEFT JOIN matricula m ON e.id = m.estudiante_id
    WHERE m.id IS NULL;
    """
    return query(sql)

# 6) Estudiantes que toman clase con MÁS de un profesor
@app.get("/estudiantes-mas-de-un-profesor")
def estudiantes_mas_de_un_profesor():
    sql = """
    SELECT e.id, e.nombre, COUNT(DISTINCT c.profesor_id) AS total_profesores
    FROM estudiante e
    JOIN matricula m ON e.id = m.estudiante_id
    JOIN curso c ON m.curso_id = c.id
    GROUP BY e.id, e.nombre
    HAVING COUNT(DISTINCT c.profesor_id) > 1;
    """
    return query(sql)

# Endpoint agrupado (opcional)
@app.get("/todo")
def todo():
    return {
        "profesores_sin_clases": profesores_sin_clases(),
        "profesores_mas_de_una_clase": profesores_mas_de_una_clase(),
        "profesores_solo_una_clase": profesores_solo_una_clase(),
        "cursos_mas_de_dos_estudiantes": cursos_mas_de_dos_estudiantes(),
        "estudiantes_sin_matriculas": estudiantes_sin_matriculas(),
        "estudiantes_mas_de_un_profesor": estudiantes_mas_de_un_profesor()
    }
