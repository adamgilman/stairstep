import unittest
from stairstep import StairStep, StatePass, StateTask
import json

class TestStepFunctionWithParameters(unittest.TestCase):
    def test_single_state_with_inputs(self):
        self.maxDiff = None
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "Hello World",
                "States": {
                    "Hello World": {
                        "Type": "Task",
                        "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
                        "End": true,
                        "InputPath": "$.lambda",
                        "OutputPath": "$.data",
                        "ResultPath": "$.data.lambdaresult"
                    }
                }
            }
        '''
        #compress and remove whitespace
        output = json.dumps( json.loads(output) )
        ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "Hello World",
        )
        hello_step = StateTask(
            name = "Hello World",
            resource = "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            end = True,
            inputpath = "$.lambda",
            outputpath = "$.data",
            resultpath = "$.data.lambdaresult"
        )

        ss.addState(hello_step)
        self.assertEqual(output, ss.json())
