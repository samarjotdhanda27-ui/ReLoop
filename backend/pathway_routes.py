from fastapi import APIRouter, HTTPException
from .geo_matching import load_json

router = APIRouter(prefix="/pathways", tags=["Reuse Pathways"])


@router.get("/{material_name}")
def get_reuse_pathways(material_name: str):

    data = load_json("reuse_pathways.json")

    if data["material"]["name"].lower() != material_name.lower():
        raise HTTPException(
            status_code=404,
            detail=f"No documented pathways found for '{material_name}'"
        )

    pathways = []

    for pathway in data["reuse_pathways"]:
        pathways.append({
            "id": pathway["id"],
            "buyer_industry": pathway["buyer_industry"],
            "application": pathway["application"],
            "relevant_properties": pathway["relevant_properties"],
            "reference_standard": pathway["reference_standard"],
            "verification_required": pathway["verification_required"],
            "evidence_sources": [
                evidence["source_id"]
                for evidence in pathway["evidence"]
            ]
        })

    return {
        "material": data["material"]["name"],
        "source_industry": data["material"]["source_industry"],
        "total_pathways": len(pathways),
        "pathways": pathways,
        "disclaimer": data["disclaimer"]
    }