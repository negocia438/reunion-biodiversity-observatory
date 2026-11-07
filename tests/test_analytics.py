import unittest

import pandas as pd

from app.analytics import annual_observations


class TestAnnualObservations(unittest.TestCase):
    def setUp(self):
        """Prépare un petit tableau avant chaque test."""
        self.observations = pd.DataFrame(
            [
                (2024, "Phelsuma", 2),
                (2024, "Furcifer", 3),
                (2025, "Phelsuma", 4),
                (2025, None, 1),
            ],
            columns=["observation_year", "genus", "observation_count"],
        )

    def test_all_genera(self):
        result = annual_observations(self.observations)
        self.assertEqual(result.to_dict(), {2024: 5, 2025: 5})

    def test_selected_genus(self):
        result = annual_observations(
            self.observations,
            selected_genus="Phelsuma",
        )
        self.assertEqual(result.to_dict(), {2024: 2, 2025: 4})

    def test_exclude_unknown_genus(self):
        result = annual_observations(
            self.observations,
            include_unknown=False,
        )
        self.assertEqual(result.to_dict(), {2024: 5, 2025: 4})

    def test_missing_genus_returns_empty_result(self):
        result = annual_observations(
            self.observations,
            selected_genus="GenreAbsent",
        )
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
