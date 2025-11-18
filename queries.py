CONSULTAS = {
    "profesores_no_clases": """
        SELECT p.numero_profesor, p.Nombre_P
        FROM profesores p
        LEFT JOIN inscripciones i ON p.numero_profesor = i.numero_profesor
        WHERE i.numero_profesor IS NULL;
    """,

    "profesores_mas_de_una_clase": """
        SELECT p.numero_profesor, p.Nombre_P, COUNT(DISTINCT i.numero_curso) AS cantidad_cursos
        FROM profesores p
        JOIN inscripciones i ON p.numero_profesor = i.numero_profesor
        GROUP BY p.numero_profesor, p.Nombre_P
        HAVING COUNT(DISTINCT i.numero_curso) > 1;
    """,

    "profesores_una_sola_clase": """
        SELECT p.numero_profesor, p.Nombre_P, COUNT(DISTINCT i.numero_curso) AS cantidad_cursos
        FROM profesores p
        JOIN inscripciones i ON p.numero_profesor = i.numero_profesor
        GROUP BY p.numero_profesor, p.Nombre_P
        HAVING COUNT(DISTINCT i.numero_curso) = 1;
    """,

    "cursos_mas_2_estudiantes": """
        SELECT m.numero_curso, m.Materias, COUNT(i.numero_estudiante) AS inscritos
        FROM materias m
        JOIN inscripciones i ON m.numero_curso = i.numero_curso
        GROUP BY m.numero_curso, m.Materias
        HAVING COUNT(i.numero_estudiante) > 2;
    """,

    "estudiantes_no_matriculados": """
        SELECT e.numero_estudiante, e.nombre
        FROM estudiantes e
        LEFT JOIN inscripciones i ON e.numero_estudiante = i.numero_estudiante
        WHERE i.numero_estudiante IS NULL;
    """,

    "estudiantes_varios_profesores": """
        SELECT e.numero_estudiante, e.nombre, COUNT(DISTINCT i.numero_profesor) AS cantidad_profesores
        FROM estudiantes e
        JOIN inscripciones i ON e.numero_estudiante = i.numero_estudiante
        GROUP BY e.numero_estudiante, e.nombre
        HAVING COUNT(DISTINCT i.numero_profesor) > 1;
    """
}
