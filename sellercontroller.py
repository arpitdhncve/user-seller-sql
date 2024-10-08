from fastapi.params import Header
from fastapi import APIRouter , status
from fastapi.responses import JSONResponse
from middleware import create_jwt, check_authorization
from sellerclass import Seller
from redishandler import save_token, get_token
from pydantic import BaseModel


router = APIRouter()


class registerRequest(BaseModel):
    name: str
    email: str



@router.post("/register-seller")
def register_seller(registerRequest: registerRequest):

    seller = Seller(registerRequest.name, registerRequest.email)

    message, success = seller.add_seller()

    if success is True:
        return JSONResponse(status_code= status.HTTP_200_OK, content = {"message" : message})
    else:
        status_code = 400 if message == "Email already registered" else 500
        return JSONResponse(status_code=status_code, content = {"detail": message})




