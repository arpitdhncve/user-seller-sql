from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from database import create_connection, create_user_table, create_seller_table
from usercontroller import router as user_router
from sellercontroller import router as seller_router



app = FastAPI()
app.include_router(user_router)
app.include_router(seller_router)


@app.on_event("startup")
def startup_event():
    create_user_table()
    create_seller_table()




@app.get("/")
def read_root():
    
    conn = create_connection()
    if conn is not None:
        conn_status = "Connected with DB"
    else:
        conn_status = "Not connected with DB"
    return JSONResponse(
        status_code= status.HTTP_200_OK,
        content = {"message": "hello world", "db_status": conn_status}
    )