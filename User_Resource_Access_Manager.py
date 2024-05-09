import aiosqlite
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import logging
import uuid
import bcrypt
from typing import List

app = FastAPI()

# Defining user model
class User(BaseModel):
    username: str
    roles: List[str]

# Initializng logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.FileHandler('api.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Basic authentication
security = HTTPBasic()

# Adding Dependency to authenticate user and retrieve roles for them
async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users WHERE username=?", (credentials.username,)) as cursor:
            user_row = await cursor.fetchone()
            if user_row is None or not bcrypt.checkpw(credentials.password.encode('utf-8'), user_row[2].encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return User(username=user_row[1], roles=user_row[3].split(','))

# Just-in-time authorization checker
async def check_access(request_id: str = None, current_user: User = Depends(get_current_user)):
    # Log current user info and request ID
    logger.info(f"Request ID: {request_id} - User {current_user.username} accessing the endpoint")
    # Performing access control checks here
    if "admin" in current_user.roles:
        return True
    else:
        message = "Access forbidden for this user."
        logger.warning(f"Request ID: {request_id} - User {current_user.username} does not have access to the endpoint")
        raise HTTPException(status_code=403, detail=message)

# Defining endpoint to access a resource
@app.get("/resource", dependencies=[Depends(check_access)])
async def get_resource():
    return {"message": "Resource can be accessed for this user."}

# Exception handler for HTTPExceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"Request ID: {request.state.request_id} - HTTPException: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

# Exception handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.exception(f"Request ID: {request.state.request_id} - Internal Server Error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

# A middleware to add unique request ID(uuid) to each request
@app.middleware("http")
async def add_request_id(request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    return response
