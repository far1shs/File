import json, os


def args():
    with open("./args.json", "r", encoding="utf-8") as file:
        args = file.read()
        file.close()
        return json.loads(args)
