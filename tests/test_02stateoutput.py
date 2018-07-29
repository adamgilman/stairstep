import unittest, json
from stairstep import StairStep, StateTask, StatePass, StateChoice, StateSucceed

class TestStateOutputPass(unittest.TestCase):
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
    
    def test_output(self):
        self.maxDiff = None
        #validated by statelint
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "HelloWorld": { 
                        "Type": "Pass",
                        "Comment": "Pass State example",
                        "End": true
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

class TestStateOutputTask(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "HelloWorld",
        )
        self.state = StateTask(
            name            = "HelloWorld",
            comment         = "Task State example",
            resource        = "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
            end             = True
        )
        self.ss.addState(self.state)
    
    def test_output(self):
        self.maxDiff = None
        #validated by statelint
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "HelloWorld": { 
                        "Type": "Task",
                        "Comment": "Task State example",
                        "Resource": "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
                        "End": true
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

class TestStateOutputSucceed(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "HelloWorld",
        )
        self.state = StateSucceed(
            name            = "HelloWorld",
            comment         = "Succeed State example",
        )
        self.ss.addState(self.state)
    
    def test_output(self):
        self.maxDiff = None
        #validated by statelint
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "HelloWorld": { 
                        "Type": "Succeed",
                        "Comment": "Succeed State example"
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

class TestStateMultiTaskOutput(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "HelloWorld",
        )
        self.first = StateTask(
            name            = "HelloWorld",
            comment         = "Task State example",
            resource        = "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
            snext           = "SecondState"
        )
        self.ss.addState(self.first)

        self.second = StateTask(
            name            = "SecondState",
            comment         = "Task State example",
            resource        = "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
            end             = True
        )
        self.ss.addState(self.second)

    
    def test_output(self):
        self.maxDiff = None
        #validated by statelint
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "HelloWorld": { 
                        "Type": "Task",
                        "Comment": "Task State example",
                        "Resource": "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
                        "Next": "SecondState"
                    },
                    "SecondState": {
                        "Type": "Task",
                        "Comment": "Task State example",
                        "Resource": "arn:aws:swf:us-east-1:123456789012:task:HelloWorld",
                        "End": true
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)