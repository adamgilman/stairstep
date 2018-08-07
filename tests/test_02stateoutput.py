import unittest, json
from stairstep import StairStep, StateTask, StatePass, StateChoice, StateSucceed, StateWait

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

class TestStateOutputWait(unittest.TestCase):
    def setUp(self):
        self.ss = StairStep(
            comment = "A simple minimal example of the States language",
            startAt = "HelloWorld",
        )        
    
    def test_output_delay(self):
        self.state = StateWait(
            name            = "wait_ten_seconds",
            seconds         = 10,
            snext           = "NextState"
        )
        self.ss.addState(self.state)

        self.maxDiff = None
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "wait_ten_seconds" : {
                        "Type" : "Wait",
                        "Seconds" : 10,
                        "Next": "NextState"
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

    def test_output_absolute(self):
        from datetime import datetime, timezone

        wait_until = datetime(year=2016, month=3, day=14, hour=1, minute=59, second=0, tzinfo=timezone.utc)
        self.state = StateWait(
            name            = "wait_until",
            timestamp       = wait_until,
            snext           = "NextState"
        )
        self.ss.addState(self.state)

        self.maxDiff = None
        #python datetime ISO export doesn't suppport Zulu, changed to +00
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "wait_until" : {
                        "Type": "Wait",
                        "Timestamp": "2016-03-14T01:59:00+00:00",
                        "Next": "NextState"
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)

    def test_output_reference_time(self):
        from datetime import datetime, timezone

        self.state = StateWait(
            name            = "wait_until",
            timestamppath   = "$.expirydate",
            snext           = "NextState"
        )
        self.ss.addState(self.state)

        self.maxDiff = None
        #python datetime ISO export doesn't suppport Zulu, changed to +00
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "wait_until" : {
                        "Type": "Wait",
                        "TimestampPath": "$.expirydate",
                        "Next": "NextState"
                    }
                }
            }
        '''
        
        output = json.loads(output)
        result = json.loads( self.ss.json() )
        self.assertDictEqual(output, result)
    
    def test_output_reference_seconds(self):
        from datetime import datetime, timezone

        self.state = StateWait(
            name            = "wait_until",
            secondspath     = "$.seconds",
            snext           = "NextState"
        )
        self.ss.addState(self.state)

        self.maxDiff = None
        #python datetime ISO export doesn't suppport Zulu, changed to +00
        output = '''
            {
                "Comment": "A simple minimal example of the States language",
                "StartAt": "HelloWorld",
                "States": {
                    "wait_until" : {
                        "Type": "Wait",
                        "SecondsPath": "$.seconds",
                        "Next": "NextState"
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