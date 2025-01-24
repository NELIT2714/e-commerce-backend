from sqlalchemy import Column, Integer, String, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from project.database import Base


class Admins(Base):
    __tablename__ = "tbl_admins"

    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(254), unique=True, index=True)
    password_hash = Column(LargeBinary)

    permissions = relationship("AdminsPermissions", back_populates="admin", uselist=True)


class AdminsPermissions(Base):
    __tablename__ = "tbl_admins_permissions"

    permission_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admins.admin_id"), index=True)
    permission = Column(String(100))

    admin = relationship("Admins", back_populates="permissions")
