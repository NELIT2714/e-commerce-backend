from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from project.database import Base


class Users(Base):
    __tablename__ = "tbl_users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), index=True)
    email = Column(String(254), unique=True, index=True)
    password_hash = Column(Text, nullable=False)

    personal_data = relationship("PersonalData", back_populates="user")
    delivery_data = relationship("DeliveryData", back_populates="user")


class PersonalData(Base):
    __tablename__ = "tbl_personal_data"

    personal_data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    first_name = Column(String(50), nullable=True, default=None)
    last_name = Column(String(50), nullable=True, default=None)
    phone_number = Column(String(20), nullable=True, default=None)

    user = relationship("Users", back_populates="personal_data")


class DeliveryData(Base):
    __tablename__ = "tbl_delivery_data"

    delivery_data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), index=True)
    country = Column(String(100), nullable=True, default=None)
    city = Column(String(100), nullable=True, default=None)
    postcode = Column(String(20), nullable=True, default=None)
    address = Column(String(255), nullable=True, default=None)

    user = relationship("Users", back_populates="delivery_data")
