from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import File, UploadFile
import tempfile
import os

app = FastAPI()


async def process_file(file):
    print(" I am calculating someone salary!")
    with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as temp_file:
        content = await file.read()
        temp_file.write(content)
        append_string = "\n SOME CLIENT DATA\n"
        temp_file.write(append_string.encode())  # Write the string to the file

        # Get the path of the temp file
        temp_file_path = temp_file.name
    return temp_file_path

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getfile")
async def root():
    return {"message": "Its sunny!"}

@app.post("/store")
async def root(file: UploadFile):
    print(file)
    with open(file.filename, "wb") as f:
        while chunk := file.file.read(1024):  # Read in chunks of 1KB
            f.write(chunk)
    return {"message": "Received file"}

@app.post("/upload")
async def root(file: UploadFile):
    temp_file_path = await process_file(file)
    # Return the modified file back to the client
    return FileResponse(temp_file_path, filename="modified_" + file.filename)

@app.get("/download_ola")
async def root():
    if os.path.exists("ola.txt"):
        return FileResponse(path="ola.txt", filename="ola.txt")
    else:
        return {"message": "OLA FILE NOT NOT FOUND"}