import os
import uuid

def save_uploaded_file(uploaded_file, storage_dir="enterprise_storage/raw_docs"):
  os.makedirs(storage_dir, exist_ok=True)
  file_ext = os.path.splitext(uploaded_file.name)[1]
  file_path = os.path.join(storage_dir, f"{uuid.uuid4()}{file_ext}")

  with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

  return file_path, uploaded_file.name