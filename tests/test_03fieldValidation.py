import unittest
from stairstep import StatePass, StateTask, StateChoice
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
        self.original_state = StatePass(
            name = "Hello World",
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
        self.original_state = StateTask(
            name = "Hello World",
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
        self.original_state = StateChoice(
            name = "Hello World",
        )
