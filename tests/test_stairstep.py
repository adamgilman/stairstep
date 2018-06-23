import unittest
from stairstep import StairStep

class TestStairStepObject(unittest.TestCase):
    def setUp(self):
        pass

    def test_base_object(self):
        ss = StairStep()
        self.assertIsInstance(ss, StairStep)