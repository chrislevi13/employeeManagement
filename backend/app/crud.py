from .database import get_db_connection
from .schemas import EmployeeCreate
import mysql.connector

def create_employee(employee: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "INSERT INTO employees (first_name, last_name, email, department, salary) VALUES (%s, %s, %s, %s, %s)"
    values = (employee.first_name, employee.last_name, employee.email, employee.department, employee.salary)
    cursor.execute(query, values)
    conn.commit()
    employee_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {**employee.dict(), "id": employee_id}

def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def update_employee(employee_id: int, employee: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "UPDATE employees SET first_name=%s, last_name=%s, email=%s, department=%s, salary=%s WHERE id=%s"
    values = (employee.first_name, employee.last_name, employee.email, employee.department, employee.salary, employee_id)
    cursor.execute(query, values)
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return None
    return {**employee.dict(), "id": employee_id}

def delete_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0
