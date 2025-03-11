from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

# Standard Libraries
import datetime as dt
from jose import jwt
import bcrypt, os

# Routers
from app.routes.first_test_router import router as FirstTestRouter

app = FastAPI()

app.include_router(FirstTestRouter, prefix="/test")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LogIn(BaseModel):
    username: str
    password: str

# The function to authenticate the whole process
def authenticate(token):
    try:
        appsecret = os.environ["appsecret"]
        payload = jwt.decode(token, appsecret)
        return {"data": payload}
    except Exception as e:
        return None
# ------------------------------------------------

# Build the LogIn functionality 
@app.post("/login")
async def login(user: LogIn):
    appsecret = os.environ["appsecret"]

    # This is where you would execute a DB call, but I using the env variables for templating
    current_user = {
        "userid": os.environ["userid"],
        "username": os.environ["username"],
        "password": os.environ["password"]
    }

    if not user.username == current_user["username"]:
        return {"status": 400, "message": "There is an error that occurred! Wrong Username!"}

    bytes_pass = user.password.encode('utf-8')

    if bcrypt.checkpw(bytes_pass, bytes(current_user["password"], 'utf-8')):
        claims = {
            'userid': current_user["userid"],
            'user': {
                'username': user.username,
                'profile': {
                    'username': user.username
                }
            },
            "exp": (dt.datetime.now() + dt.timedelta(days=3)).timestamp() # "days", here sets the days in the future we want the token to expire
        }
        
        token = jwt.encode(
            claims=claims,
            key=appsecret,
            algorithm='HS256'
        )
        return {"access_token": token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
