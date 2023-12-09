from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from app.s3 import upload_file_to_s3, list_files_in_s3, download_file_from_s3, delete_file_from_s3
from app.s3 import AWS_BUCKET_NAME
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "testuser"
    correct_password = "testpassword"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...), username: str = Depends(authenticate_user)):
#     object_name = f"uploads/{file.filename}"
#     upload_file_to_s3(file, AWS_BUCKET_NAME, object_name)
#     return {"file_name": file.filename, "object_name": object_name}

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...), username: str = Depends(authenticate_user)):
#     object_name = f"uploads/{file.filename}"
#     upload_file_to_s3(file, AWS_BUCKET_NAME, object_name)
#     return {"file_name": file.filename, "object_name": object_name}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    object_name = f"uploads/{file.filename}"
    upload_file_to_s3(file, AWS_BUCKET_NAME, object_name)
    return {"file_name": file.filename, "object_name": object_name}



# @app.get("/listfiles/")
# async def list_files(username: str = Depends(authenticate_user)):
#     files = list_files_in_s3(AWS_BUCKET_NAME)
#     return {"files": files}

@app.get("/listfiles/")
async def list_files():
    files = list_files_in_s3(AWS_BUCKET_NAME)    
    return {"files": files}

@app.get("/downloadfile/{file_name}")
async def download_file(file_name: str, username: str = Depends(authenticate_user)):
    object_name = f"uploads/{file_name}"
    return download_file_from_s3(AWS_BUCKET_NAME, object_name)

# @app.delete("/deletefile/{file_name}")
# async def delete_file(file_name: str, username: str = Depends(authenticate_user)):
#     object_name = f"uploads/{file_name}"
#     delete_file_from_s3(AWS_BUCKET_NAME, object_name)
#     return {"message": f"File {file_name} deleted successfully"}

@app.delete("/deletefile/{file_name}")
async def delete_file(file_name: str):
    object_name = f"uploads/{file_name}"
    delete_file_from_s3(AWS_BUCKET_NAME, object_name)
    return {"message": f"File {file_name} deleted successfully"}


