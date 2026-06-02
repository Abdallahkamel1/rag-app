from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File,status
import os
from helpers.config import get_settings
from controllers import DataController
from controllers import ProjectController
import aiofiles
from models import ResponseEnum
from schemas import ProcessRequest
from controllers import ProcessController


data_router = APIRouter()

@data_router.post("/upload/{project_id}")
async def upload_data(project_id : str, file: UploadFile,
                     app_settings = Depends(get_settings)):

    data_controller = DataController()
    is_valid, response_signal = await data_controller.validate_uploaded_file(project_id, file)
    project_controller = ProjectController()


    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST
        ,content= {"response_signal" : response_signal.value})
    
    project_path = project_controller.get_project_path(project_id)

    file_path = os.path.join(project_path, file.filename)

    async with aiofiles.open(file_path, mode="wb") as f:
        while chunk := await file.read(app_settings.default_chunk_size):
            await f.write(chunk)
            
    return JSONResponse(
        content= {"response_signal" : ResponseEnum.FILE_UPLOADED.value
                   , "file_name" : file.filename
                    })    

        
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, request: ProcessRequest):
    process_controller = ProcessController(project_id)
    file_id = request.file_id
    chunk_size = request.chunk_size
    chunk_overlap = request.chunk_overlap
    file_chunks = process_controller.process_file_content(file_id,chunk_size,chunk_overlap)

    if file_chunks == None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
        content={"response_signal": ResponseEnum.FILE_PROCESSING_FAILED.value})

    return file_chunks    
    

    
                     
    