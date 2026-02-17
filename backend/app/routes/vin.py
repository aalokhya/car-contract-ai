from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/vin/{vin}")
def decode_vin(vin: str):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    return requests.get(url).json()
