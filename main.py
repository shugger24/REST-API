from fastapi import FastAPI

items = [
    {"name": "Computer", "preis": 1000, "typ": "hardware"},
    {"name": "Laptop", "preis": 1200, "typ": "hardware"},
    {"name": "Maus", "preis": 25, "typ": "zubehör"},
    {"name": "Tastatur", "preis": 45, "typ": "zubehör"},
    {"name": "Monitor", "preis": 300, "typ": "hardware"},
    {"name": "Drucker", "preis": 150, "typ": "hardware"},
    {"name": "Headset", "preis": 80, "typ": "zubehör"},
    {"name": "Externe Festplatte", "preis": 90, "typ": "speicher"},
    {"name": "USB-Stick", "preis": 15, "typ": "speicher"},
    {"name": "Grafikkarte", "preis": 600, "typ": "hardware"},
    {"name": "Mainboard", "preis": 250, "typ": "hardware"}
]

app = FastAPI()

@app.get("/items/")
async def show():
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return items[item_id]
