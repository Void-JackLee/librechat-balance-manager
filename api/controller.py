from fastapi import APIRouter, Depends, Form, HTTPException
from .result import err,ok
from .cmd import list_balances, set_balance
import yaml

app = APIRouter()

with open("config/config.yml", "r") as f:
    config = yaml.safe_load(f)
compose_path = config.get("compose-path", "docker-compose.yml")
exclude_email = config.get("exclude-email", [])

@app.get("/list-balances")
def _list_balances():
    # Implementation for listing balances
    result = list_balances(compose_path)
    result = [item for item in result if item["email"] not in exclude_email]
    return ok(result)

@app.post("/set-balance")
def _set_balance(email: str = Form(...), balance: float = Form(...)):
    set_balance(compose_path, balance, email)
    return ok()

@app.post("/set-all-balances")
def _set_all_balances(balance: float = Form(...)):
    set_balance(compose_path, balance)
    return ok()
