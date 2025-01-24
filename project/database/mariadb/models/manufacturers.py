from sqlalchemy import Column, Integer, String

from project.database import Base


class Manufacturers(Base):
    __tablename__ = "manufacturers"

    manufacturer_id = Column(Integer, primary_key=True, index=True)
    manufacturer_name = Column(String(30), index=True)
