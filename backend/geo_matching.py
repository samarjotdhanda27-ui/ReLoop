import json
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    """Load JSON data from the ReLoop data directory."""
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate straight-line distance between two coordinates in km."""

    coordinates = [lat1, lon1, lat2, lon2]

    if not all(math.isfinite(float(value)) for value in coordinates):
        raise ValueError("Coordinates must be finite numbers")

    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("Latitude must be between -90 and 90")

    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("Longitude must be between -180 and 180")

    earth_radius = 6371.0

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        coordinates
    )

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return round(earth_radius * c, 2)


def find_nearby_buyers(
    seller,
    buyers,
    pathways,
    max_distance_km=300,
    supported_material="Fly Ash"
):
    """
    Find potential buyers using material type, documented reuse
    pathways, geographic distance, and quantity availability.

    This is decision support, not industrial safety certification.
    """

    results = []

    seller_material = seller["material"].strip().casefold()
    supported_material = supported_material.strip().casefold()

    # Prevent unsupported materials from using fly ash pathways.
    if seller_material != supported_material:
        return []

    if max_distance_km <= 0:
        raise ValueError("Maximum distance must be greater than zero")

    if seller["available_quantity_tonnes"] <= 0:
        raise ValueError("Seller quantity must be greater than zero")

    for buyer in buyers:

        if buyer["facility_type"] != "buyer":
            continue

        buyer_material = buyer["required_material"].strip().casefold()

        if buyer_material != seller_material:
            continue

        matching_pathway = next(
            (
                pathway
                for pathway in pathways
                if pathway["buyer_industry"].strip().casefold()
                == buyer["industry"].strip().casefold()
            ),
            None
        )

        if matching_pathway is None:
            continue

        distance = haversine_distance(
            seller["latitude"],
            seller["longitude"],
            buyer["latitude"],
            buyer["longitude"]
        )

        if distance > max_distance_km:
            continue

        quantity_available = seller["available_quantity_tonnes"]
        quantity_required = buyer["required_quantity_tonnes"]

        quantity_sufficient = quantity_available >= quantity_required

        reasons = [
            f"Documented potential reuse pathway: {matching_pathway['application']}",
            f"Buyer is approximately {distance} km away (straight-line distance)"
        ]

        if quantity_sufficient:
            reasons.append(
                f"Available quantity ({quantity_available} tonnes) "
                f"meets buyer demand ({quantity_required} tonnes)"
            )
        else:
            reasons.append(
                f"Insufficient quantity: buyer needs {quantity_required} tonnes, "
                f"but seller has {quantity_available} tonnes"
            )

        results.append({
            "buyer_id": buyer["id"],
            "buyer_name": buyer["name"],
            "industry": buyer["industry"],
            "city": buyer["city"],
            "state": buyer["state"],
            "latitude": buyer["latitude"],
            "longitude": buyer["longitude"],
            "distance_km": distance,
            "quantity_sufficient": quantity_sufficient,
            "quantity_required_tonnes": quantity_required,
            "pathway_id": matching_pathway["id"],
            "reuse_application": matching_pathway["application"],
            "reasons": reasons,
            "verification_required": matching_pathway.get(
                "verification_required", True
            ),
            "match_status": (
                "Potential Match"
                if quantity_sufficient
                else "Insufficient Quantity"
            ),
            "is_synthetic": buyer.get("is_synthetic", False)
        })

    return sorted(
        results,
        key=lambda item: (
            not item["quantity_sufficient"],
            item["distance_km"]
        )
    )


if __name__ == "__main__":

    facilities_data = load_json("facilities.json")
    pathways_data = load_json("reuse_pathways.json")

    facilities = facilities_data["facilities"]
    pathways = pathways_data["reuse_pathways"]

    seller = next(
        facility
        for facility in facilities
        if facility["id"] == "FAC001"
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
        supported_material=pathways_data["material"]["name"]
    )

    print("\nRELOOP GEOGRAPHIC MATCHING RESULTS")
    print("-----------------------------------")
    print(f"Seller: {seller['name']}")
    print(f"Material: {seller['material']}\n")

    for index, match in enumerate(matches, start=1):
        print(
            f"{index}. {match['buyer_name']}\n"
            f"   Industry: {match['industry']}\n"
            f"   Distance: {match['distance_km']} km\n"
            f"   Reuse Pathway: {match['reuse_application']}\n"
            f"   Status: {match['match_status']}\n"
        )

        print("   Match Explanations:")

        for reason in match["reasons"]:
            print(f"   - {reason}")

        print()