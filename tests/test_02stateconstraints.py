import unittest, json
from stairstep import State

class TestStateBaseConstraints(unittest.TestCase):
    def test_must_have_type(self):
        '''All states MUST have a “Type” field.'''
        bad_state = State(
            name = "InvalidState",
            resource="arn:fake",
            end=False
        )
        
        with self.assertRaises(AttributeError):
            bad_state.export()

    def test_may_have_comment(self):
        '''Any state MAY have a “Comment” field'''
        output = {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                "Next" : "nextResource",
            }
        no_comment = State(
            name = "Hello World",
            stype = "Task",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            snext = "nextResource",
        )
        self.assertEqual( no_comment.export(), output )

        output = {
                "Comment": "Comments may be present",
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                "Next" : "nextResource",
            }
        has_comment = State(
            name = "Hello World",
            comment = "Comments may be present",
            stype = "Task",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            snext = "nextResource",
        )
        self.assertEqual( has_comment.export(), output )

    def test_may_have_end_state(self):
        '''Any state except for Choice, Succeed, and Fail MAY 
        have a field named "End" whose value MUST be a boolean.
        The term “Terminal State” means a state with with { "End": true },
        or a state with { "Type": "Succeed" }, 
        or a state with { "Type": "Fail" }.
        '''

        choice_cannot_end = State(
            name = "Hello World",
            stype = "Choice",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            choice_cannot_end.export()

        succeed_cannot_end = State(
            name = "Hello World",
            stype = "Succeed",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            succeed_cannot_end.export()

        fail_cannot_end = State(
            name = "Hello World",
            stype = "Fail",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            fail_cannot_end.export()
        
class TestStateNonTerminalStates(unittest.TestCase):
    '''
    All non-terminal states MUST have a “Next” field, 
    except for the Choice state. The value of the “Next” 
    field MUST exactly and case-sensitively match the 
    name of the another state.
    '''
    def test_non_terminal_must_have_next(self):
        states = ["Pass","Task","Choice","Wait","Succeed","Fail","Parallel"]
        for s in states:
            task = State(
                name = "Hello World",
                stype = s,
                resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                end = True
            )
            if s not in ['Succeed', 'Fail']:
                with self.assertRaises(AttributeError):
                    task.export()
    

class TestStateTerminalStates(unittest.TestCase):
    pass