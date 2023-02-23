from typing import Dict
from toml import loads
import re


def format_template(template: str, vars: Dict[str, str]):
    for key, value in vars.items():
        regex = r"{{" + re.escape(key) + r"}}"
        template = template.replace(regex, value)

    return template


def load_toml():
    json = ""
    with open("./email.toml") as file:
        json = loads(file.read())

    return json
