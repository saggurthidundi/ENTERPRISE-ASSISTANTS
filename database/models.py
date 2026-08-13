import uuid
from datetime import datetime
from database.connection import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"
  id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  email = Column(String, unique=True, index=True, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")

class Document(Base):
  __tablename__ = "documents"
  id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  filename = Column(String, nullable=False)
  file_path = Column(Text, nullable=False)
  file_type = Column(String, nullable=False)
  owner_id = Column(String, ForeignKey("users.id"))
  created_at = Column(DateTime, default=datetime.utcnow)
  owner = relationship("User", back_populates="documents")
  chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
  __tablename__ = "document_chunks"
  id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
  document_id = Column(String, ForeignKey("documents.id"))
  content = Column(Text, nullable=False)
  chunk_index = Column(Integer, nullable=False)
  document = relationship("Document", back_populates="chunks")