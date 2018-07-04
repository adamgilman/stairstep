import unittest
from stairstep import State
from .sharedFieldValidation import FieldValidationTests

class TestStatePassState(unittest.TestCase, FieldValidationTests):
    def setUp(self):
        self.state_fields = {
            'required_fields' : ['stype'],
            'allowed_fields'  : ['comment', 'inputpath', 'outputpath'],
            'not_allowed'     : ['retry', 'catch']
        }

        #if True, next or catch MUST be True
        self.next_or_end = True
        self.original_state = State(
            name = "Hello World",
            stype = "Pass",
            snext = "nextResource",
        )

class TestStateTaskState(unittest.TestCase, FieldValidationTests):
    def setUp(self):
        self.state_fields = {
            'required_fields' : ['stype'],
            'allowed_fields'  : ['comment', 'inputpath', 'outputpath', 'retry', 'catch'],
            'not_allowed'     : []
        }

        #if True, next or catch MUST be True
        self.next_or_end = True
        self.original_state = State(
            name = "Hello World",
            stype = "Task",
            snext = "nextResource",
        )

class TestStateChoiceState(unittest.TestCase, FieldValidationTests):
    def setUp(self):
        self.state_fields = {
            'required_fields' : ['stype'],
            'allowed_fields'  : ['comment', 'inputpath', 'outputpath'],
            'not_allowed'     : ['retry', 'catch']
        }

        #if True, next or catch MUST be True
        self.next_or_end = False
        self.original_state = State(
            name = "Hello World",
            stype = "Choice",
        )
