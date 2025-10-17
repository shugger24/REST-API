from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from jose import jwt
from enum import Enum
from typing import Optional

items = [
    {"name": "Computer", "preis": 1000, "typ": "hardware"},
    {"name": "Laptop", "preis": 1200, "typ": "hardware"},
    {"name": "Game1", "preis": 25, "typ": "software"},
    {"name": "Game2", "preis": 45, "typ": "software"},
    {"name": "Monitor", "preis": 300, "typ": "hardware"},
    {"name": "Drucker", "preis": 150, "typ": "hardware"},
    {"name": "GameZ", "preis": 80, "typ": "software"},
    {"name": "GameY", "preis": 90, "typ": "software"},
    {"name": "GameX", "preis": 15, "typ": "software"},
    {"name": "Grafikkarte", "preis": 600, "typ": "hardware"},
    {"name": "Mainboard", "preis": 250, "typ": "hardware"}
]

class Type(Enum):
    hardware = "hardware"
    software = "software"


class Item(BaseModel):
    name: str
    preis: int = Field(100, gt=0, lt=2500)
    typ: Type

class ResponseItem(BaseModel):
    name: str
    typ: Type

app = FastAPI()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    if data.username == "test" and data.password == "test":
        access_token = jwt.encode({"user": data.username}, key="secret")
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    

# Endpunkte
#@app.get("/items/")
#async def show_all_items(token: str = Depends(oauth2_schema)):
#    jwt.decode(token)
#    return items

@app.get("/items/")
async def show_all_items(q: Optional[str] = None):
    if q:
        data = []
        for item in items:
            if item.get("typ") == q:
                data.append(item)
        return data
    return items

@app.get("/items/{item_id}", dependencies=[Depends(oauth2_schema)])
async def get_item(item_id: int):
    return items[item_id]

@app.post("/items/", response_model=ResponseItem)
async def create_item(data: Item):
    items.append(data)
    return data

@app.put("/items/{item_id}", dependencies=[Depends(oauth2_schema)])
async def change_item(item_id: int, item: Item):
    items[item_id] = item
    return item

@app.delete("/items/{item_id}", dependencies=[Depends(oauth2_schema)])
async def delete_item (item_id: int):
    item = items[item_id]
    items.pop(item_id)
    return {"deleted": item}
