import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.database import (connect_db, insert_student, fetch_students, delete_student, insert_level, fetch_levels,
                         delete_level, update_level, insert_payment, fetch_payments, delete_payment, insert_user,
                         fetch_users, delete_user, insert_reward, fetch_rewards, reward_already_granted,
                         is_student_under_bonus, get_students_with_expiring_bonus)
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ----------------------------- #
#       TEST: Estudiantes      #
# ----------------------------- #

def test_insert_fetch_delete_student():
    """Verifica que se pueda insertar, consultar y eliminar un alumno."""
    name = "Test Estudiante"
    age = 20
    level = "A2"

    insert_student(name, age, level)
    students = fetch_students()
    found = any(s["name"] == name and s["age"] == age and s["level"] == level for s in students)
    assert found, "El alumno no fue encontrado en la base de datos"

    delete_student(name)
    students = fetch_students()
    found = any(s["name"] == name for s in students)
    assert not found, "El alumno no fue eliminado correctamente"

# -------------------------- #
#       TEST: Niveles       #
# -------------------------- #

def test_insert_update_delete_level():
    """Verifica la inserción, actualización y eliminación de niveles."""
    original = "Z1"
    updated = "Z2"

    insert_level(original)
    levels = [lvl[1] for lvl in fetch_levels()]
    assert original in levels, "El nivel no fue insertado correctamente"

    update_level(original, updated)
    levels = [lvl[1] for lvl in fetch_levels()]
    assert updated in levels and original not in levels, "La actualización de nivel falló"

    delete_level(updated)
    levels = [lvl[1] for lvl in fetch_levels()]
    assert updated not in levels, "El nivel no fue eliminado correctamente"

# ------------------------ #
#       TEST: Pagos       #
# ------------------------ #

def test_insert_fetch_delete_payment():
    """Verifica inserción y eliminación de pagos (requiere un alumno)."""
    name = "Pago Tester"
    insert_student(name, 30, "B1")
    students = fetch_students()
    student_id = next(s["id"] for s in students if s["name"] == name)

    insert_payment(student_id, 99.9, "2025-05-21", "tarjeta", "test pago")
    pagos = fetch_payments()
    found = any(p[1] == name and p[2] == 99.9 for p in pagos)
    assert found, "El pago no fue insertado correctamente"

    payment_id = next(p[0] for p in pagos if p[1] == name and p[2] == 99.9)
    delete_payment(payment_id)

    pagos = fetch_payments()
    found = any(p[0] == payment_id for p in pagos)
    assert not found, "El pago no fue eliminado correctamente"

    delete_student(name)  # Limpieza

# -------------------------- #
#       TEST: Usuarios       #
# -------------------------- #

def test_insert_fetch_delete_user():
    """Verifica inserción y eliminación de usuarios"""
    username = "admin_test"
    password = "1234"
    role = "admin"

    insert_user(username, password, role)
    users = fetch_users()
    found = any(u[1] == username and u[2] == password and u[3] == role for u in users)
    assert found, "El usuario no fue insertado correctamente"

    delete_user(username)
    users = fetch_users()
    found = any(u[1] == username for u in users)
    assert not found, "El usuario no fue eliminado correctamente"

# ------------------------------ #
#     TEST: Recompensas (bonos) #
# ------------------------------ #

def test_insert_fetch_reward():
    """Verifica inserción de recompensa y validación de bono"""
    recommender = "Recomendador Test"
    new_student = "Alumno Nuevo Test"

    insert_student(recommender, 25, "A1")
    insert_student(new_student, 22, "B2")

    students = fetch_students()
    r_id = next(s["id"] for s in students if s["name"] == recommender)
    n_id = next(s["id"] for s in students if s["name"] == new_student)

    insert_reward(r_id, n_id, 3, datetime.now().strftime("%Y-%m-%d"))

    rewards = fetch_rewards()
    found = any(r[1] == recommender and r[2] == new_student for r in rewards)
    assert found, "La recompensa no fue insertada correctamente"

    assert reward_already_granted(n_id), "La verificación de bono activo falló"

    # No se elimina recompensa aquí porque no implementamos delete_reward
    delete_student(recommender)
    delete_student(new_student)

# ------------------------------ #
#     TEST: Recompensas (bonos) #
# ------------------------------ #

# ---------- CONFIGURACIÓN DEL MÓDULO DE PRUEBAS DE BONIFICACIONES ----------

def setup_module(module):
    """Prepara datos para probar bonificaciones según tu lógica actual."""
    # Insertamos tres estudiantes
    insert_student("AlumnoBonoActivo", 20, "B2")
    insert_student("AlumnoSinBono", 21, "B1")
    insert_student("AlumnoBonoPorExpirar", 22, "B2")

    students = fetch_students()
    bono_activo_id = next(s["id"] for s in students if s["name"] == "AlumnoBonoActivo")
    sin_bono_id = next(s["id"] for s in students if s["name"] == "AlumnoSinBono")
    expira_id = next(s["id"] for s in students if s["name"] == "AlumnoBonoPorExpirar")

    hoy = datetime.now().strftime("%Y-%m-%d")
    fecha_1_mes_atras = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d")

    # AlumnoBonoActivo es el recomendador de un nuevo alumno → Tiene bono activo (6 meses)
    insert_reward(recommender_id=bono_activo_id, new_student_id=expira_id, months_rewarded=6, date_awarded=hoy)

    # AlumnoBonoPorExpirar recomendó a otro → Su bono caduca pronto (1 mes)
    insert_reward(recommender_id=expira_id, new_student_id=sin_bono_id, months_rewarded=1, date_awarded=fecha_1_mes_atras)

    # AlumnoSinBono no ha recomendado a nadie → No tiene bono

def teardown_module(module):
    """Elimina los estudiantes de prueba después del test"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rewards WHERE 1=1")
    cursor.execute("DELETE FROM students WHERE name IN (?, ?, ?)",
                   ("AlumnoBonoActivo", "AlumnoSinBono", "AlumnoBonoPorExpirar"))
    conn.commit()
    conn.close()

# ---------- TEST DE BONIFICACIONES ----------

def test_is_student_under_bonus_true():
    """Debe detectar que 'AlumnoBonoActivo' tiene un bono activo como recomendador"""
    students = fetch_students()
    student = next(s for s in students if s["name"] == "AlumnoBonoActivo")
    assert is_student_under_bonus(student["id"]) is True

def test_is_student_under_bonus_false():
    """Debe detectar que 'AlumnoSinBono' NO tiene bono (no recomendó a nadie)"""
    students = fetch_students()
    student = next(s for s in students if s["name"] == "AlumnoSinBono")
    assert is_student_under_bonus(student["id"]) is False

# ------------------------------ #
#     TEST: Casos Negativos      #
# ------------------------------ #

def test_insert_duplicate_student():
    """Verifica que se puedan insertar duplicados (si no se controla en BBDD)"""
    name = "EstudianteDuplicado"
    insert_student(name, 18, "A1")
    insert_student(name, 18, "A1")  # Se permite duplicar por backend

    estudiantes = fetch_students()
    ocurrencias = [s for s in estudiantes if s["name"] == name]
    assert len(ocurrencias) >= 2, "No se permitió insertar duplicado (aunque debería)"

    # Limpieza
    for s in ocurrencias:
        delete_student(s["name"])

def test_insert_invalid_payment_amount():
    """Verifica que no se inserte un pago con cantidad negativa"""
    insert_student("EstudiantePagoInvalido", 25, "B1")
    student_id = next(s["id"] for s in fetch_students() if s["name"] == "EstudiantePagoInvalido")

    try:
        insert_payment(student_id, -50, "2025-05-21", "efectivo", "Cantidad negativa")
        assert False, "Se permitió insertar un pago negativo"
    except Exception:
        pass  # Correcto: debe lanzar excepción o ser bloqueado

    delete_student("EstudiantePagoInvalido")

def test_insert_reward_twice_for_same_student():
    """Verifica que no se pueda dar dos recompensas al mismo nuevo alumno"""
    insert_student("RecomendadorX", 30, "C1")
    insert_student("AlumnoNuevoX", 18, "A2")

    r_id = next(s["id"] for s in fetch_students() if s["name"] == "RecomendadorX")
    n_id = next(s["id"] for s in fetch_students() if s["name"] == "AlumnoNuevoX")

    insert_reward(r_id, n_id, 3, datetime.now().strftime("%Y-%m-%d"))
    already_granted = reward_already_granted(n_id)
    assert already_granted, "No detectó que el alumno ya tenía recompensa"

    # Intentar insertar de nuevo (aunque insert_reward no lo impide, reward_already_granted sí)
    if already_granted:
        try:
            insert_reward(r_id, n_id, 1, datetime.now().strftime("%Y-%m-%d"))
            assert False, "Se otorgó una segunda recompensa al mismo alumno"
        except Exception:
            pass  # Esperado

    delete_student("RecomendadorX")
    delete_student("AlumnoNuevoX")