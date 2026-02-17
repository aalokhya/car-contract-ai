from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from app.db.session import get_db
from app.services.sla_extractor import extract_sla, detect_risks, fairness_score
from app.services.negotiation_ai import generate_tips
from app.services.report_generator import generate_report

router = APIRouter()


@router.post("/analyze/{contract_id}")
def analyze_contract(contract_id: int, db: Session = Depends(get_db)):

    # Fetch contract text from database
    result = db.execute(
        text("SELECT content FROM contracts WHERE id=:id"),
        {"id": contract_id}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_text = result[0]

    # SLA extraction
    sla_data = extract_sla(contract_text)

    # Risk detection
    risks = detect_risks(contract_text)

    # Fairness score
    score = fairness_score(risks)

    # Negotiation tips
    tips = generate_tips(contract_id, risks)

    return {
        "contract_id": contract_id,
        "summary": sla_data,
        "risks": risks,
        "fairness_score": score,
        "tips": tips
    }


@router.get("/download/{contract_id}")
def download_report(contract_id: int, db: Session = Depends(get_db)):

    # Fetch contract text again
    result = db.execute(
        text("SELECT content FROM contracts WHERE id=:id"),
        {"id": contract_id}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_text = result[0]

    # Re-run analysis
    sla_data = extract_sla(contract_text)
    risks = detect_risks(contract_text)
    score = fairness_score(risks)
    tips = generate_tips(contract_id, risks)

    analysis = {
        "summary": sla_data,
        "risks": risks,
        "fairness_score": score,
        "tips": tips
    }

     # Generate report
    file_path = generate_report(contract_id, analysis)

    return FileResponse(
        path=file_path,
        filename=f"contract_report_{contract_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )