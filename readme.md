# FastAPI Example Project

## Overview
This repository contains a minimal FastAPI application that demonstrates:
- Basic REST API structure  
- JWT-based authentication using OAuth2  
- Data validation with Pydantic models  
- Enum usage for controlled data types  

The application maintains an in-memory list of items (hardware and software) and provides CRUD operations with authentication for protected routes.

---

## Features
- **Login endpoint** using static demo credentials  
- **Token-based authentication** with OAuth2PasswordBearer  
- **Data validation** via Pydantic models  
- **Filtering support** on `/items/` endpoint  
- **CRUD functionality** (`GET`, `POST`, `PUT`, `DELETE`)  

---

## Endpoints

### `POST /login`
Authenticates a user with demo credentials and returns a JWT access token.

**Demo credentials:**
- Username: `test`  
- Password: `test`

### `GET /items/`
Returns all items.  
Optional query parameter `q` filters by type (`hardware` or `software`).

### `GET /items/{item_id}`
Returns a specific item by index.  
Requires a valid bearer token.

### `POST /items/`
Creates a new item.  
Validates input using the `Item` Pydantic model and returns a filtered response model (`ResponseItem`).

### `PUT /items/{item_id}`
Updates an existing item.  
Requires a valid bearer token.

### `DELETE /items/{item_id}`
Deletes an item by index.  
Requires a valid bearer token.

---

## Technologies
- **Python 3.10+**  
- **FastAPI** for API framework  
- **Pydantic** for data validation  
- **python-jose** for JWT handling  
- **OAuth2PasswordBearer** for authentication  

---

## Installation and Execution

```bash
# Create a virtual environment
python -m venv venv
# Activate the environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install fastapi uvicorn python-jose
# Start the development server
uvicorn main:app --reload


Notes
The application uses hardcoded credentials and a static JWT secret.
Do not use this implementation in a production environment without proper security adjustments.