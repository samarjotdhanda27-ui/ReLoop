from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .geo_matching import load_json, find_nearby_buyers


router = APIRouter(
    prefix="/geo",
    tags=["Geographic Matching"]
)


class SellerInput(BaseModel):
    id: str
    name: str
    facility_type: str = "seller"
    industry: str
    city: str
    state: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    material: str
    available_quantity_tonnes: float = Field(gt=0)
    is_synthetic: bool = False


class BuyerInput(BaseModel):
    id: str
    name: str
    facility_type: str = "buyer"
    industry: str
    city: str
    state: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    required_material: str
    required_quantity_tonnes: float = Field(gt=0)
    is_synthetic: bool = False


class GeographicMatchRequest(BaseModel):
    seller: SellerInput
    buyers: List[BuyerInput]
    max_distance_km: float = Field(default=300, gt=0)


@router.get("/matches/{seller_id}")
def get_geographic_matches(seller_id: str):

    facilities = load_json("facilities.json")["facilities"]

    pathway_data = load_json("reuse_pathways.json")
    pathways = pathway_data["reuse_pathways"]
    supported_material = pathway_data["material"]["name"]

    seller = next(
        (
            facility
            for facility in facilities
            if facility["id"] == seller_id
            and facility["facility_type"] == "seller"
        ),
        None
    )

    if seller is None:
        raise HTTPException(
            status_code=404,
            detail="Seller not found"
        )

    buyers = [
        facility
        for facility in facilities
        if facility["facility_type"] == "buyer"
    ]

    matches = find_nearby_buyers(
        seller=seller,
        buyers=buyers,
        pathways=pathways,
        max_distance_km=300,
        supported_material=supported_material
    )

    return {
        "seller_id": seller["id"],
        "seller_name": seller["name"],
        "seller_location": {
            "latitude": seller["latitude"],
            "longitude": seller["longitude"]
        },
        "total_matches": len(matches),
        "matches": matches,
        "data_type": "synthetic_demo"
    }


@router.post("/calculate")
def calculate_geographic_matches(request: GeographicMatchRequest):

    pathway_data = load_json("reuse_pathways.json")
    pathways = pathway_data["reuse_pathways"]
    supported_material = pathway_data["material"]["name"]

    seller = request.seller.model_dump()

    buyers = [
        buyer.model_dump()
        for buyer in request.buyers
    ]

    matches = find_nearby_buyers(
        seller=seller,
        buyers=buyers,
        pathways=pathways,
        max_distance_km=request.max_distance_km,
        supported_material=supported_material
    )

    return {
        "seller_id": seller["id"],
        "seller_name": seller["name"],
        "seller_location": {
            "latitude": seller["latitude"],
            "longitude": seller["longitude"]
        },
        "total_matches": len(matches),
        "matches": matches,
        "data_type": (
            "synthetic_demo"
            if seller["is_synthetic"] or any(
                buyer["is_synthetic"] for buyer in buyers
            )
            else "user_submitted"
        ),
        "disclaimer": (
            "Results are preliminary reuse and geographic suggestions. "
            "They do not certify material suitability, safety, or compliance."
        )
    }