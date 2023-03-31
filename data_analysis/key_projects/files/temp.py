
import json

with open("key_completers_03-08-23.json", "r", encoding="utf-8") as file:
    d = json.load(file)

with open("temp.csv", "w", encoding="utf-8") as file:
    for p in d.values():
        name = p["consent"]["CF2"]
        email = p["demographics"]["Q12"]
        file.write(",".join((name,email,"\n")))

print(len(d))
