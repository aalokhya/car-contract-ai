from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.db.session import get_db
from app.services.text_extractor import extract_text
from sqlalchemy import text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_contract(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text(file_path)

    result = db.execute(
        text("INSERT INTO contracts (filename, content) VALUES (:f, :c) RETURNING id"),
        {"f": file.filename, "c": extracted_text}
    )

    contract_id = result.fetchone()[0]
    db.commit()

    return {
        "contract_id": contract_id,
        "filename": file.filename,
        "status": "uploaded"
    }
