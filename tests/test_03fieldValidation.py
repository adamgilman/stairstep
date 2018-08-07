import unittest
from unittest import TestCase
from stairstep import StatePass, StateTask, StateChoice, StateSucceed, StateFail, StateWait
from stairstep.base import StateBase

from stairstep.validations import *

class FieldValidationsTests(unittest.TestCase):
    def setUp(self):
        self.state = StateBase()
    
    def test_non_terminal_must_have_next(self):
        self.state.next = None
        with self.assertRaises(AttributeError):
            validation_none_terminal_must_have_next(self.state)

        self.state.end = True
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
    
    def test_end_cannot_be_true(self):
        self.state.end = True
        with self.assertRaises(AttributeError):
            validation_end_cannot_be_true(self.state)

    def test_not_allowed_to_have_path_fields(self):
        self.state.inputpath = "$.ipath"
        with self.assertRaises(AttributeError):
            validation_cannot_have_io_path_fields(self.state)

        self.state.inputpath = None

        self.state.outputpath = "$.opath"
        with self.assertRaises(AttributeError):
            validation_cannot_have_io_path_fields(self.state)

class StateFieldValidationsTests(unittest.TestCase):
    def setUp(self):
        self.state = StateWait(
            snext = "NextField"
        )
    #A Wait state MUST contain exactly one of Seconds, SecondsPath, Timestamp, or TimestampPath.

    def test_wait_must_contain_time_field(self):
        #has no fields    
        with self.assertRaises(AttributeError):
            validation_must_contain_only_one_time_field(self.state)
        
    def test_wait_must_contain_has_at_least_one(self):
        self.state.secondspath = "$.seconds"    
        validation_must_contain_only_one_time_field(self.state)

    def test_wait_must_contain_only_one(self):
        self.state.seconds = 11
        self.state.secondspath = "$.seconds"    
        with self.assertRaises(AttributeError):
            validation_must_contain_only_one_time_field(self.state)


class StateTestCases(unittest.TestCase):
    class CommonTests(unittest.TestCase):
        def test_all_state_validations(self):
            all_validations = [
                validation_states_cant_have_both_end_and_next,
                validation_name_cannot_be_longer_than_128,
                validation_all_states_must_have_type
            ]
            
            for v in all_validations:
                self.assertIn(v, self.state.base_validations)

#TODO allowed_operators = ["StringEquals","StringLessThan","StringGreaterThan","StringLessThanEquals","StringGreaterThanEquals","NumericEquals","NumericLessThan","NumericGreaterThan","NumericLessThanEquals","NumericGreaterThanEquals","BooleanEquals","TimestampEquals","TimestampLessThan","TimestampGreaterThan","TimestampLessThanEquals","TimestampGreaterThanEquals","And","Or","Not"]

class TestPassStateValidations(StateTestCases.CommonTests):
    def setUp(self):
        self.state = StatePass()
    def test_required_validations(self):
        required = [
            validation_none_terminal_must_have_next,
            validation_states_must_have_next_or_end    
        ]
        self.assertCountEqual(required, self.state.validations)

class TestChoiceStateValidations(StateTestCases.CommonTests):
    def setUp(self):
        self.state = StateChoice()
    def test_required_validations(self):
        required = [
            validation_end_cannot_be_true
        ]
        self.assertCountEqual(required, self.state.validations)

class TestSucceedStateValidations(StateTestCases.CommonTests):
    def setUp(self):
        self.state = StateSucceed()
    def test_required_validations(self):
        required = [
            validation_end_cannot_be_true
        ]
        self.assertCountEqual(required, self.state.validations)

class TestFailStateValidations(StateTestCases.CommonTests):
    def setUp(self):
        self.state = StateFail()
    def test_required_validations(self):
        required = [
            validation_end_cannot_be_true,
            validation_cannot_have_io_path_fields
        ]
        self.assertCountEqual(required, self.state.validations)

class TestWaitStateValidations(StateTestCases.CommonTests):    
    def setUp(self):
        self.state = StateWait()
    def test_required_validations(self):
        required = [
            validation_must_contain_only_one_time_field
        ]
        self.assertCountEqual(required, self.state.validations)