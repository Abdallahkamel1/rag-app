from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseEnum

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.scale = 1024 * 1024

    async def validate_uploaded_file(self, project_id: str, file: UploadFile):

        if file.content_type not in self.app_settings.file_allowed_types:
            return False , ResponseEnum.TYPE_NOT_ALLOWED.value

        if file.size > (self.app_settings.file_max_size * self.scale):
            return False , ResponseEnum.SIZE_EXCEEDED.value

        return True , ResponseEnum.FILE_VALIDATED_SUCCESS.value  
        
