from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from database import Base



class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    geneset_id = Column(Integer, ForeignKey("genesets.id"))

    geneset = relationship("Geneset", back_populates="genes")



class Geneset(Base):
    __tablename__ = "genesets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    genes = relationship("Gene", back_populates="geneset")
