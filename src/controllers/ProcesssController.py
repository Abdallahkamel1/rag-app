from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
import os
from models.enums.ProcessEnums import ProcessEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    def __init__(self , project_id):
        super().__init__()
        self.project_id = project_id
        
        self.project_path = ProjectController().get_project_path(self.project_id)

    def get_file_extension(self , file_id: str):
        file_extension = os.path.splitext(file_id)[-1]
        return file_extension

    def get_file_loader(self , file_id : str):
        file_extension = self.get_file_extension(file_id)
        if file_extension == ProcessEnum.TXT.value:
            return TextLoader(os.path.join(self.project_path, file_id) , encoding="utf-8")
        elif file_extension == ProcessEnum.PDF.value:
            return PyMuPDFLoader(os.path.join(self.project_path, file_id))
        else:
            return None

    def get_file_content(self , file_id : str):
        file_loader = self.get_file_loader(file_id)
        return file_loader.load()

    def process_file_content(self , file_id:str,chunk_size:int , chunk_overlap:int):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
        )

        file_content = self.get_file_content(file_id)

        page_contents = [
            rec.page_content 
            for rec in file_content
        ]

        meta_data = [
            rec.metadata
            for rec in file_content
        ]

        file_chunks = text_splitter.create_documents(page_contents,metadatas=meta_data)

        return file_chunks
  
    
                            

             


    