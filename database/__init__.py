from database.connection import Base, SessionLocal, engine, get_db
from database.models import Document, DocumentChunk, User

def init_sample_data():
  Base.metadata.create_all(bind=engine)
  db = SessionLocal()
  try:
    if not db.query(User).first():
      admin_user = User(email="admin@enterprise.ai")
      db.add(admin_user)
      db.commit()
  finally:
    db.close()

init_sample_data()