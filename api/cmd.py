import subprocess
import re
from tqdm import tqdm

def remove_ansi_escape(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)

def list_balances(yml_location):
    cmd = ["docker-compose", "-f", yml_location, "exec", "api", "sh", "-c", "cd /app && npm run list-balances"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    result = result.stdout.strip()
    result = result.split('-----------------------------')[-1]
    result = remove_ansi_escape(result)
    result = result.splitlines()[1:-1]
    
    data = []
    for line in result:
        line = line.strip()
        name = line[5:line.find("(")-1]
        email = line[line.find("(")+1:line.find(")")]
        balance = 0 if line.find("no balance") != -1 else float(line.split("balance of ")[-1])
        data.append({
            "name": name,
            "email": email,
            "balance": balance
        })
    if __name__ == "__main__":
        for item in data:
            print(f"Name: {item['name']}, Email: {item['email']}, Balance: {item['balance']}")
    return data

def set_balance(yml_location, balance: float, email: str = None):
    if email:
        cmd = ["docker-compose", "-f", yml_location, "exec", "api", "sh", "-c", f"cd /app && npm run set-balance {email} {balance}"]
        subprocess.run(cmd)
    else:
        for item in tqdm(list_balances(yml_location)):
            cmd = ["docker-compose", "-f", yml_location, "exec", "api", "sh", "-c", f"cd /app && npm run set-balance {item['email']} {balance}"]
            subprocess.run(cmd)


if __name__ == "__main__":
    import click

    @click.group()
    @click.argument("compose_path", default="docker-compose.yml")
    @click.pass_context
    def cli(ctx, compose_path):
        ctx.ensure_object(dict)
        ctx.obj["compose_path"] = compose_path

    @cli.command(name="list-balances")
    @click.pass_context
    def _list_balances(ctx):
        """
        List all user balances.
        """
        list_balances(ctx.obj["compose_path"])

    @cli.command(name="set-balance")
    @click.pass_context
    @click.argument("balance", type=float)
    @click.option("--email", "-e", help="Filter by user email", default=None)
    def _set_balance(ctx, balance: float, email: str = None):
        """
        Set the balance for a user.
        """
        set_balance(ctx.obj["compose_path"], balance, email)
    
    cli()