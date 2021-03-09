import json


def get_inventory_data():
    with open('data/inventory.json') as f:
        return json.load(f)
