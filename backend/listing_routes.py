from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .database import get_supabase


router = APIRouter(tags=["Marketplace Listings"])


# ==========================================
# SELLER MATERIAL MODEL
# ==========================================

class MaterialCreate(BaseModel):

    seller_name: str = Field(min_length=2)
    material_name: str = Field(min_length=2)
    source_industry: str = Field(min_length=2)

    quantity_tonnes: float = Field(gt=0)

    city: str = Field(min_length=2)
    state: str = Field(min_length=2)

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    material_properties: dict[str, Any] = Field(
        default_factory=dict
    )

    available_documents: list[str] = Field(
        default_factory=list
    )

    is_synthetic: bool = False


# ==========================================
# BUYER REQUIREMENT MODEL
# ==========================================

class RequirementCreate(BaseModel):

    buyer_name: str = Field(min_length=2)
    buyer_industry: str = Field(min_length=2)

    required_material: str = Field(min_length=2)
    required_quantity_tonnes: float = Field(gt=0)

    city: str = Field(min_length=2)
    state: str = Field(min_length=2)

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    required_properties: dict[str, Any] = Field(
        default_factory=dict
    )

    required_documents: list[str] = Field(
        default_factory=list
    )

    is_synthetic: bool = False


# ==========================================
# CREATE SELLER LISTING
# ==========================================

@router.post("/materials", status_code=201)
def create_material(material: MaterialCreate):

    try:

        supabase = get_supabase()

        response = (
            supabase.table("materials")
            .insert(material.model_dump())
            .execute()
        )

        return {
            "message": "Material listing created successfully",
            "material": response.data[0]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to save material listing"
        )


# ==========================================
# GET ALL MATERIAL LISTINGS
# ==========================================

@router.get("/materials")
def get_materials():

    try:

        supabase = get_supabase()

        response = (
            supabase.table("materials")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "total_materials": len(response.data),
            "materials": response.data
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve materials"
        )


# ==========================================
# CREATE BUYER REQUIREMENT
# ==========================================

@router.post("/requirements", status_code=201)
def create_requirement(requirement: RequirementCreate):

    try:

        supabase = get_supabase()

        response = (
            supabase.table("buyer_requirements")
            .insert(requirement.model_dump())
            .execute()
        )

        return {
            "message": "Buyer requirement created successfully",
            "requirement": response.data[0]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to save buyer requirement"
        )


# ==========================================
# GET ALL BUYER REQUIREMENTS
# ==========================================

@router.get("/requirements")
def get_requirements():

    try:

        supabase = get_supabase()

        response = (
            supabase.table("buyer_requirements")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return {
            "total_requirements": len(response.data),
            "requirements": response.data
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve buyer requirements"
        )