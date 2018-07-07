import unittest
from unittest import TestCase
from stairstep import StatePass, StateTask, StateChoice
from stairstep.base import StateBase

from stairstep.validations import *

#TODO: Create individual validations, and test isolated
#TODO: Test that tasks have required validations

class FieldValidationsTests(unittest.TestCase):
    def setUp(self):
        self.state = StateBase()
    
    def test_non_terminal_must_have_next(self):
        self.state.next = None
        with self.assertRaises(AttributeError):
            validation_none_terminal_must_have_next(self.state)

    def test_states_must_have_next_or_end(self):
        self.state.next = None
        self.state.end = None
        with self.assertRaises(AttributeError):
            validation_states_must_have_next_or_end(self.state)
    
    def test_states_cant_have_both_end_and_next(self):
        self.state.next = "NextResource"
        self.state.end = True
        with self.assertRaises(AttributeError):
            validation_states_cant_have_both_end_and_next(self.state)
    
    def test_name_longer_than_128(self):
        self.state.name = "a" * 129
        with self.assertRaises(AttributeError):
            validation_name_cannot_be_longer_than_128(self.state)

    def test_states_must_have_type(self):
        self.state.stype = None
        with self.assertRaises(AttributeError):
            validation_all_states_must_have_type(self.state)

class StateTestCases:
    class CommonTests(unittest.TestCase):
        def test_all_state_validations(self):
            all_validations = [
                validation_states_cant_have_both_end_and_next,
                validation_name_cannot_be_longer_than_128,
            ]
            
            for v in all_validations:
                self.assertIn(v, self.state.base_validations)


class TestPassStateValidations(StateTestCases.CommonTests):
    def setUp(self):
        self.state = StatePass()
    def test_required_validations(self):
        required = [
            validation_none_terminal_must_have_next,
            validation_states_must_have_next_or_end    
        ]
        self.assertCountEqual(required, self.state.validations)
