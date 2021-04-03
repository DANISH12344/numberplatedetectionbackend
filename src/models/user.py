from sqlalchemy import Column, Integer, Text, String
from src.database.db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    img = Column(Text())
    result_number = Column(String(400))
    def __init__(self,
                 img=None,
                 result_number = None,
                 ):
        self.img=img
        self.result_number = result_number

    def toDict(self):
        u = {"Image":self.img, "Number": self.result_number}
        return u

