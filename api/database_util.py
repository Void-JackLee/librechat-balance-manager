from mongoengine import connect
import yaml

with open("config/config.yml", "r") as f:
    config = yaml.safe_load(f)
db_config = config.get("db")

print(f"Init with:\n{db_config}")
connect(
    db=db_config['name'],
    host=db_config['host'],
    port=db_config["port"]
)