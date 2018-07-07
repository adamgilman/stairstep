import unittest, json
from stairstep import StateTask, StateChoice, StateSucceed, StateFail

class TestStateBaseConstraints(unittest.TestCase):
    def test_may_have_comment(self):
        '''Any state MAY have a “Comment” field'''
        output = {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                "Next" : "nextResource",
            }
        no_comment = StateTask(
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
        has_comment = StateTask(
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

        choice_cannot_end = StateChoice(
            name = "Hello World",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            choice_cannot_end.export()

        succeed_cannot_end = StateSucceed(
            name = "Hello World",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            succeed_cannot_end.export()

        fail_cannot_end = StateFail(
            name = "Hello World",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True
        )
        with self.assertRaises(AttributeError):
            fail_cannot_end.export()
        