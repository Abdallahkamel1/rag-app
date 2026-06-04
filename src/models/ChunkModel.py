from models.enums.DataBaseEnum import DataBaseEnum
from .BaseDataModel import BaseDataModel
# pyrefly: ignore [missing-import]
from pymongo import InsertOne
from .db_schemas.data_chunk import DataChunk
from bson.objectid import ObjectId

class ChunkModel(BaseDataModel):
    
    def __init__(self , db_client):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.CHUNKS_COLLECTION_NAME.value]
    async def create_chunk(self , chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_none=True))
        chunk.id = result.inserted_id
        return chunk
    async def get_chunk(self , chunk_id:str):
        result = await self.collection.find_one({"_id" : chunk_id})
        if result is None:
            return None

        return DataChunk(**result)

    async def insert_many_chunks(self , chunks: list[DataChunk] , batch_size= 100):

        for i in range(0 , len(chunks) , batch_size):
            batch = chunks[i:i+batch_size]
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_none=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)

    async def delete_chunks_by_project_id(self , project_id: ObjectId):
        result = await self.collection.delete_many({'chunk_project_id' : project_id})
        return result.deleted_count    

        
    
   