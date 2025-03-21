import unittest
from data_viewer import vprint


class TestDataViewer(unittest.TestCase):
    def test_vprint(self):
        data = {"key": "value", "nested": {"inner_key": "inner_value"}}
        try:
            vprint(data, var_name="test_data")
        except Exception as e:
            self.fail(f"vprint raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
