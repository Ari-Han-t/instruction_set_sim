# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from assembler_sim import assemble, execute

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Home page for entering assembly code."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "output": None,
        "registers": None,
        "flags": None,
        "memory": None
    })


@app.post("/run", response_class=HTMLResponse)
def run_program(request: Request, code: str = Form(...)):
    """Handle assembly input, execute simulation, and return results."""
    assembled = assemble(code)
    log, registers, memory = execute(assembled)

    # Compute flags
    zero_flag = 1 if any(r == 0 for r in registers) else 0
    carry_flag = 0  # optional future expansion

    output = "\n".join(log)
    reg_status = "\n".join([f"R{i} = {val}" for i, val in enumerate(registers)])
    mem_view = "\n".join([f"[{i}] = {val}" for i, val in enumerate(memory) if val != 0])
    flags = f"Zero Flag (Z) = {zero_flag}\nCarry Flag (C) = {carry_flag}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "output": output,
        "registers": reg_status,
        "memory": mem_view if mem_view else "All memory cells are 0",
        "flags": flags,
        "code": code
    })
