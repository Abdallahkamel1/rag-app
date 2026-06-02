from enum import Enum
class ResponseEnum(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully"
    TYPE_NOT_ALLOWED = "File type not allowed"  
    SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOADED = "File uploaded successfully"
    FILE_NOT_UPLOADED = "File not uploaded"
    FILE_PROCESSING_FAILED = "File processing failed"
    FILE_PROCESSING_SUCCESS = "File processing successful" 