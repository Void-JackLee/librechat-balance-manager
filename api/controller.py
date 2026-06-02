from fastapi import APIRouter, Depends, Form, HTTPException, Body
from .result import err,ok
from .service import get_balance, get_user, set_balance
import yaml

app = APIRouter()

exclude_email = None
credit_scale = None
credit_field_name = None
email_field_name = None

def load_config():
    global exclude_email, credit_scale, credit_field_name, email_field_name

    with open("config/config.yml", "r") as f:
        config = yaml.safe_load(f)
    exclude_email = config.get("exclude-email", [])
    credit_scale = config.get("credit-scale", 1/3)
    credit_field_name = config.get("credit-field-name")
    email_field_name = config.get("email-field-name")

@app.get("/list-balances")
def _list_balances():
    # Implementation for listing balances
    load_config()
    result = [ {"name": user.name, "email": user.email, "balance": balance.token_credits if balance else 0} for user, balance in get_balance()]
    result = [item for item in result if item["email"] not in exclude_email]
    return ok(result)

@app.post("/set-balance")
def _set_balance(email: str = Form(...), balance: float = Form(...)):
    set_balance(email, balance)
    return ok()

@app.post("/set-all-balances")
def _set_all_balances(balance: float = Form(...)):
    users = get_user()
    for user in users:
        try:
            set_balance(user.email, balance)
        except Exception as e:
            print(e)
    return ok()

@app.get("/get-json-field-hint")
def _get_json_field_hint():
    load_config()
    data = [{
        credit_field_name: f"<credit_value> * {credit_scale}",
        email_field_name: "<email_value>"
    }]
    return ok(data)

@app.post("/set-balances-from-json")
def _set_balances_from_json(data: list[dict] = Body(...)):
    load_config()
    emails = []
    credits = []
    for item in data:
        emails.append(item.get(email_field_name))
        credits.append(item.get(credit_field_name))
    
    all_balance = get_balance()
    available_emails = {}
    for user, balance in all_balance:
        if balance:
            available_emails[user.email] = 1
    wrong_emails = []
    for email in emails:
        if email not in available_emails:
            wrong_emails.append(email)
    if len(wrong_emails) > 0:
        print(wrong_emails)
        raise HTTPException(status_code=400, detail=f"以下{len(wrong_emails)}个邮箱不存在: {', '.join(wrong_emails)}")
    for email, credit in zip(emails, credits):
        if credit is None:
            credit = 1000e6
        try:
            set_balance(email, credit * credit_scale)
        except Exception as e:
            print(e)
    return ok()

