import unittest
from stairstep import StairStep, StatePass

class TestStairStepObject(unittest.TestCase):
    def setUp(self):
        pass

    def test_base_object(self):
        ss = StairStep()
        self.assertIsInstance(ss, StairStep)

class TestStairStepIndempodent(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "HelloWorld",
        )
        self.state = StatePass(
            name            = "HelloWorld",
            comment         = "Pass State example",
            end             = True
        )
        self.ss.addState(self.state)
        
    def test_export_is_indempodent(self):
        self.ss.export()
        self.ss.export()
