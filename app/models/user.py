from app.db.base import DataBase
from dotenv import load_dotenv
from typing import List
import os

class User:
    def __init__(self):        
        # Load environment variables from .env file
        load_dotenv()

        self.__db_url = os.environ.get('DB_URL')
        self.__db_name = os.environ.get('DB_NAME')
        self.__table_name = os.environ.get('USER_TABLE_NAME')
        self.__db = DataBase(db_url=self.__db_url)
        

    def save(self, data: dict):        
        return  self.__db.upload(db_name=self.__db_name, table_name=self.__table_name, data=data)

    def get(self, user_uuid: int):
        return self.__db.query(db_name=self.__db_name, table_name=self.__table_name, filter={"user_uuid": user_uuid})

    def get_all(self):
        return list(self.__db.query(db_name=self.__db_name, table_name=self.__table_name, bulk=True))

    def filter(self, filter: dict):
        return list(self.__db.query(db_name=self.__db_name, table_name=self.__table_name, filter=filter, bulk=True))
    
    def update(self, data: dict):
        return self.__db.update(db_name=self.__db_name, table_name=self.__table_name, data=data)

    def delete(self, filter: dict):
        return self.__db.delete(db_name=self.__db_name, table_name=self.__table_name, filter=filter)