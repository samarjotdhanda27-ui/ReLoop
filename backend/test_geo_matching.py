import unittest
from copy import deepcopy

from backend.geo_matching import (
    haversine_distance,
    find_nearby_buyers,
    load_json
)


class TestGeoMatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.facilities = load_json("facilities.json")["facilities"]
        cls.pathways = load_json("reuse_pathways.json")["reuse_pathways"]

        cls.seller = next(
            facility
            for facility in cls.facilities
            if facility["id"] == "FAC001"
        )

        cls.buyers = [
            facility
            for facility in cls.facilities
            if facility["facility_type"] == "buyer"
        ]

    def test_distance_calculation(self):
        distance = haversine_distance(
            30.478,
            76.593,
            30.3782,
            76.7767
        )

        self.assertAlmostEqual(distance, 20.82, places=2)

    def test_all_eight_buyers_found(self):
        matches = find_nearby_buyers(
            self.seller,
            self.buyers,
            self.pathways
        )

        self.assertEqual(len(matches), 8)

    def test_nearest_buyer(self):
        matches = find_nearby_buyers(
            self.seller,
            self.buyers,
            self.pathways
        )

        self.assertEqual(
            matches[0]["buyer_id"],
            "FAC003"
        )

    def test_incompatible_material(self):
        modified_buyer = deepcopy(self.buyers[0])

        modified_buyer["required_material"] = "Steel Slag"

        matches = find_nearby_buyers(
            self.seller,
            [modified_buyer],
            self.pathways
        )

        self.assertEqual(len(matches), 0)

    def test_insufficient_quantity(self):
        modified_buyer = deepcopy(self.buyers[0])

        modified_buyer["required_quantity_tonnes"] = 1000

        matches = find_nearby_buyers(
            self.seller,
            [modified_buyer],
            self.pathways
        )

        self.assertEqual(len(matches), 1)

        self.assertFalse(
            matches[0]["quantity_sufficient"]
        )

        self.assertEqual(
            matches[0]["match_status"],
            "Insufficient Quantity"
        )

    def test_distance_limit(self):
        matches = find_nearby_buyers(
            self.seller,
            self.buyers,
            self.pathways,
            max_distance_km=10
        )

        self.assertEqual(len(matches), 0)

    def test_invalid_industry(self):
        modified_buyer = deepcopy(self.buyers[0])

        modified_buyer["industry"] = "Textile Manufacturing"

        matches = find_nearby_buyers(
            self.seller,
            [modified_buyer],
            self.pathways
        )

        self.assertEqual(len(matches), 0)

    def test_explanations_present(self):
        matches = find_nearby_buyers(
            self.seller,
            self.buyers,
            self.pathways
        )

        self.assertIn("reasons", matches[0])
        self.assertGreater(len(matches[0]["reasons"]), 0)

    def test_pathway_id_present(self):
        matches = find_nearby_buyers(
            self.seller,
            self.buyers,
            self.pathways
        )

        self.assertIn("pathway_id", matches[0])


if __name__ == "__main__":
    unittest.main()