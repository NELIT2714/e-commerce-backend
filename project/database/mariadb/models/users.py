from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from project.database import Base


class Users(Base):
    __tablename__ = "tbl_users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(254), unique=True, index=True)
    password_hash = Column(LargeBinary(60), nullable=False)

    sessions = relationship("Sessions", back_populates="user", uselist=True)
    personal_data = relationship("PersonalData", back_populates="user", uselist=False)
    delivery_data = relationship("DeliveryData", back_populates="user", uselist=False)


class PersonalData(Base):
    __tablename__ = "tbl_users_personal_data"

    personal_data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), index=True)
    first_name = Column(String(50), nullable=True, default=None)
    last_name = Column(String(50), nullable=True, default=None)
    phone_number = Column(String(20), nullable=True, default=None)

    user = relationship("Users", back_populates="personal_data")


class DeliveryData(Base):
    __tablename__ = "tbl_users_delivery_data"

    delivery_data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), index=True)
    country = Column(String(100), nullable=True, default=None)
    city = Column(String(100), nullable=True, default=None)
    postcode = Column(String(20), nullable=True, default=None)
    address = Column(String(255), nullable=True, default=None)

    user = relationship("Users", back_populates="delivery_data")


class Sessions(Base):
    __tablename__ = "tbl_users_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbl_users.user_id"), index=True)
    token = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates="sessions")
    data = relationship("SessionsData", back_populates="session", uselist=False)


class SessionsData(Base):
    __tablename__ = "tbl_users_sessions_data"

    session_data_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("tbl_users_sessions.session_id"), index=True)
    os = Column(String(50), nullable=False)
    browser = Column(String(50), nullable=False)
    device = Column(String(100), nullable=False)
    ip = Column(String(20), nullable=False)

    session = relationship("Sessions", back_populates="data")

