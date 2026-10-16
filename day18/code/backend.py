from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER, SECRET, ALGORITHM
import pymysql
import jwt
import datetime
import json


# create a structure for login input
class LoginRequest(BaseModel):
    username: str
    password: str


def get_user_details(username: str, password: str):
    # open connection with mysql database
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )

    # get the cursor
    with connection.cursor() as cursor:
        cursor.execute("select * from users where username = %s and password = %s", (username, password))
        result = cursor.fetchone()

    # close the connection
    connection.close()
    return result


# create a server
app = FastAPI(title="MCP Demo application")


@app.post("/login")
def login(request: LoginRequest):
    # get the user details
    user = get_user_details(request.username, request.password)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid user name or password")

    # get the current date and time
    now = datetime.datetime.now()

    # generate payload
    payload = {"sub": user["username"], "permissions": json.loads(user["permissions"]), "aud": "mcp_demo"}

    # generate the jwt token
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {"access_token": token, "permissions": user["permissions"]}


# run the backend
# uvicorn backend.py:app --port 8001 --reload

# get the swagger uri
# open http://localhost:8001/docs
