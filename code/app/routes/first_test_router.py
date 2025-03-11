from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

# Standard Libraries
from jose import jwt
import os

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# The function to authenticate the whole process
def authenticate(token):
    try:
        appsecret = os.environ["appsecret"]
        payload = jwt.decode(token, appsecret)
        return {"data": payload}
    except Exception as e:
        return None
# ------------------------------------------------

@router.get("/creative_data")
async def creative_data(input: str, token: Annotated[str, Depends(oauth2_scheme)]):
    response = authenticate(token)

    if not response:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return {"response": "You said: {}".format(input)}