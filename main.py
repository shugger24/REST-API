from fastapi import FastAPI, Depends, HTTPException, status # Import FastAPI core classes and functions
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer # Import OAuth2 security utilities
from pydantic import BaseModel, Field # Import Pydantic for data validation
from jose import jwt # Import JWT for token encoding/decoding
from enum import Enum # Import Enum for fixed value types
from typing import Optional # Import Optional for optional type hints

# Example data list of items (acts as in-memory database)
items = [
    {"name": "Desktop PC", "preis": 1000, "typ": "hardware"},
    {"name": "Laptop Pro", "preis": 1200, "typ": "hardware"},
    {"name": "Racing Simulator", "preis": 25, "typ": "software"},
    {"name": "Space Adventure", "preis": 45, "typ": "software"},
    {"name": "4K Monitor", "preis": 300, "typ": "hardware"},
    {"name": "Laser Printer", "preis": 150, "typ": "hardware"},
    {"name": "Zombie Attack", "preis": 80, "typ": "software"},
    {"name": "Mystery Quest", "preis": 90, "typ": "software"},
    {"name": "Puzzle World", "preis": 15, "typ": "software"},
    {"name": "Graphics Card RTX", "preis": 600, "typ": "hardware"},
    {"name": "Motherboard X570", "preis": 250, "typ": "hardware"}
]

class Type(Enum): # Enum for allowed item types
    hardware = "hardware"
    software = "software"


class Item(BaseModel): # Pydantic model for incoming item data
    name: str # Item name
    preis: int = Field(100, gt=0, lt=2500) # Price with validation constraints (0 < preis < 2500)
    typ: Type # Item type (hardware/software)

class ResponseItem(BaseModel):  # Model for API response after creating an item
    name: str
    typ: Type

app = FastAPI() # Initialize FastAPI application
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")  # Define POST endpoint for user login
async def login(data: OAuth2PasswordRequestForm = Depends()): # Automatically extract username/password form data
    if data.username == "test" and data.password == "test": # Simple static credential check
        access_token = jwt.encode({"user": data.username}, key="secret") # Encode JWT with username and secret key
        return {"access_token": access_token, "token_type": "bearer"} # Return token and type
    raise HTTPException( # Raise HTTP 401 if credentials invalid
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

#@app.get("/items/")
#async def show_all_items(token: str = Depends(oauth2_schema)):
#    jwt.decode(token)
#    return items

@app.get("/items/")
async def show_all_items(q: Optional[str] = None): # Optional query parameter 'q' for filtering
    if q: # If 'q' is provided
        data = [] # Create empty list for filtered results
        for item in items: # Iterate over all items
            if item.get("typ") == q: # Match item type with query
                data.append(item) # Add to result list
        return data # Return filtered items
    return items # Return all items if no query provided

@app.get("/items/{item_id}", dependencies=[Depends(oauth2_schema)]) # Protected GET endpoint by OAuth2 token
async def get_item(item_id: int): # Retrieve specific item by index
    return items[item_id] # Return item at given index

@app.post("/items/", response_model=ResponseItem) # POST endpoint to create new item
async def create_item(data: Item):
    items.append(data)
    return data 

@app.put("/items/{item_id}", dependencies=[Depends(oauth2_schema)]) # Protected PUT endpoint to update item
async def change_item(item_id: int, item: Item):
    items[item_id] = item
    return item

@app.delete("/items/{item_id}", dependencies=[Depends(oauth2_schema)]) # Protected DELETE endpoint
async def delete_item (item_id: int):
    item = items[item_id]
    items.pop(item_id)
    return {"deleted": item}

