from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from project.database import Base


class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)

    translations = relationship("CategoriesTranslations", back_populates="category", uselist=True)


class CategoriesTranslations(Base):
    __tablename__ = "categories_translations"

    translation_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), index=True)
    language = Column(String(5), nullable=False)
    category_name = Column(String(30), nullable=False)

    category = relationship("Categories", back_populates="translations")
