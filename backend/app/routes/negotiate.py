from fastapi import APIRouter
from app.services.negotiation_ai import generate_tips

router = APIRouter()

@router.get("/negotiate/{contract_id}")
def negotiate(contract_id: int):
    tips = generate_tips(contract_id)
    return {
        "contract_id": contract_id,
        "negotiation_tips": tips
    }
