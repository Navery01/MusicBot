
import yaml
import json
with open("config.yml", "r") as file:
    CONFIG = yaml.safe_load(file)

with open ('champions.json', "r") as file:
    CHAMPIONS = json.load(file)