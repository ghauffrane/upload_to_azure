from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from azure.storage.blob.aio import BlobServiceClient
from typing import List
import logging

app = FastAPI()

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    name = file.filename
    return await uploadtoazure(file,name,type)

@app.post("/uploadfiles/")
async def batch_upload_file(files: List[UploadFile] ):
    for f in files:
        name = f.filename
        await uploadtoazure(f,name)

    return "Files uploaded!"


async def uploadtoazure(file: UploadFile,file_name: str):
    connect_str = "DefaultEndpointsProtocol=https;AccountName=datastoragedellatf;AccountKey=HAiMRPUxiQXyiggBQilIibHTtivNwRg9+zt778MpiWBMQUGBt/S9aX+Fplv2v4QFnhoi5tC03siX+ASthJEbFA==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "todo"
    async with blob_service_client:
            container_client = blob_service_client.get_container_client(container_name)
            try:
                blob_client = container_client.get_blob_client(file_name)
                f = await file.read()
                await blob_client.upload_blob(f)
            except Exception as e:
                logging.info(e)
                return HTTPException(401, "Something went terribly wrong..")
    
    return f"{file_name} uploaded to azure container todo!"

@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )  