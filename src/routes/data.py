from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File,status , Request
import os
from helpers.config import get_settings
from controllers import DataController
from controllers import ProjectController
import aiofiles
from models import ResponseEnum
from schemas import ProcessRequest
from controllers import ProcessController
from models.db_schemas.data_chunk import DataChunk
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel


data_router = APIRouter()

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id : str, file: UploadFile,
                     app_settings = Depends(get_settings)):

    data_controller = DataController()
    is_valid, response_signal = await data_controller.validate_uploaded_file(project_id, file)
    project_controller = ProjectController()

    project_model = ProjectModel(db_client=request.app.mongodb)
    project = await project_model.get_project_or_create_one(project_id =project_id)

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
                   }
                       )    

        
@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request , project_id: str, process_request: ProcessRequest):

    project_model = ProjectModel(db_client=request.app.mongodb)
    project = await project_model.get_project_or_create_one(project_id =project_id)

    process_controller = ProcessController(project_id)
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap
    do_reset = process_request.do_reset
    

    file_chunks = process_controller.process_file_content(file_id,chunk_size,chunk_overlap)

    if file_chunks == None or len(file_chunks) == 0:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
        content={"response_signal": ResponseEnum.FILE_PROCESSING_FAILED.value})

    chunks = [
        DataChunk(
            chunk_text = chunk.page_content,
            chunk_metadata = chunk.metadata,
            chunk_order = i+1,
            chunk_project_id = project.id
        )
        for i , chunk in enumerate(file_chunks)
    ]

    chunk_model = ChunkModel(db_client = request.app.mongodb)

    if do_reset:
        await chunk_model.delete_chunks_by_project_id(project.id)


    no_records = await chunk_model.insert_many_chunks(chunks)

    return {"no_records" : no_records}
        
