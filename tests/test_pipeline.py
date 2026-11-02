import unittest
import pandas as pd
from scripts.metric_depth_sweep import run

class TestPipeline(unittest.TestCase):
    def test_depth_sweep(self):
        df = pd.DataFrame({
            "region": ["A"] * 6 + ["B"] * 6,
            "HIT_1": list(range(6)) * 2,
            "fish_a": list(range(6)) * 2,
            "fish_b": [x * 2 for x in range(6)] * 2,
        })
        result = run(df, metric_count=1, max_depth=3, metrics=None, responses=None)
        self.assertFalse(result.empty)
        self.assertEqual(set(result.Ecoregion), {"A", "B"})
        self.assertTrue(result.Depth.between(1, 3).all())

if __name__ == "__main__":
    unittest.main()
