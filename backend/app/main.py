from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from . import crud, database
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables if they don't exist
    database.create_tables()
    yield
    # Shutdown logic (if any) can go here

app = FastAPI(title="Employee Management System", lifespan=lifespan)

# Templates and Static Files
templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    employees = crud.get_employees()
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

@app.post("/add")
async def add_employee(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    salary: float = Form(...)
):
    from .schemas import EmployeeCreate
    employee = EmployeeCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        department=department,
        salary=salary
    )
    crud.create_employee(employee)
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{employee_id}")
async def remove_employee(employee_id: int):
    crud.delete_employee(employee_id)
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{employee_id}", response_class=HTMLResponse)
async def edit_page(request: Request, employee_id: int):
    employee = crud.get_employee(employee_id)
    employees = crud.get_employees()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "employees": employees,
        "edit_employee": employee
    })

@app.post("/update/{employee_id}")
async def update_employee_record(
    employee_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    salary: float = Form(...)
):
    from .schemas import EmployeeCreate
    employee = EmployeeCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        department=department,
        salary=salary
    )
    crud.update_employee(employee_id, employee)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
