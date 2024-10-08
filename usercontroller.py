from fastapi.params import Header
from fastapi import APIRouter , status
from fastapi.responses import JSONResponse
from userclass import User
from pydantic import BaseModel
from middleware import create_jwt, check_authorization
from redishandler import save_token, get_token

router = APIRouter()


class registerRequest(BaseModel):
    name: str
    email: str


@router.post("/user_register")
def register_user(registerRequest : registerRequest):

    user = User(registerRequest.name, registerRequest.email)
    message, success = user.add_user()

    if success is True:
        return JSONResponse(status_code= status.HTTP_200_OK, content = {"message" : message})
    else:
        status_code = 400 if message == "Email already registered" else 500
        return JSONResponse(status_code=status_code, content = {"detail": message})





class verifyOtp(BaseModel):
    email : str
    otp : int



@router.post("/verify-user")
def verify_otp(verifyOtp : verifyOtp):
    message, success = User.verify_user_otp(verifyOtp.email, verifyOtp.otp)

    if success is True:
        token = create_jwt(verifyOtp.email)
        save_token(verifyOtp.email, token)
        return JSONResponse(status_code= status.HTTP_202_ACCEPTED, content = {"message" : message, "authToken": token})
    else : 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content = {"detail" : message})








class login(BaseModel):
    email : str




@router.post("/login-user")
def login_user(login: login):
    email = login.email
    message, success = User.login_user(email)

    if success:
        return JSONResponse(
            status_code= status.HTTP_202_ACCEPTED,
            content = {"message" : message}
        )
    else:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content = {"details": message}
        )







class protected(BaseModel):
    email : str


@router.get("/protected-endpoint")
def protected(protected: protected, authorization = Header(None)):
    message , success = check_authorization(protected.email, authorization)
    if success:
        return JSONResponse(
            status_code= status.HTTP_200_OK,
            content = {"message": message}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content = {"details": message}
        )
  










